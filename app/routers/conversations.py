from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models import Conversation, Message, User
from app.schemas import ConversationCreate, ConversationOut, MessageOut

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationOut)
async def create_conversation(
    body: ConversationCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    convo = Conversation(user_id=user.id, title=body.title)
    db.add(convo)
    await db.commit()
    await db.refresh(convo)
    return convo


@router.get("", response_model=list[ConversationOut])
async def list_conversations(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Conversation).where(Conversation.user_id == user.id)
    )
    return result.scalars().all()


@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
async def get_messages(
    conversation_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    convo = (
        await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user.id,
            )
        )
    ).scalar_one_or_none()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    return result.scalars().all()
