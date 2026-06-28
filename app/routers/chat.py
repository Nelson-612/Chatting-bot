from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.llm.provider import get_provider
from app.memory.buffer import BufferMemory
from app.models import Conversation, Message, User
from app.schemas import ChatRequest, ChatResponse
from app.tokenizer import count_tokens

router = APIRouter(prefix="/chat", tags=["chat"])

# v1 uses the buffer strategy. As you build the others, swap this one line
# (or make it configurable per request) -- that's the payoff of the interface.
strategy = BufferMemory()
provider = get_provider()


@router.post("/{conversation_id}", response_model=ChatResponse)
async def send_message(
    conversation_id: int,
    body: ChatRequest,
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

    # 1. persist the incoming user message (count tokens ONCE, here)
    user_msg = Message(
        conversation_id=convo.id,
        role="user",
        content=body.content,
        token_count=count_tokens(body.content),
    )
    db.add(user_msg)
    await db.flush()  # make it visible to the query below within this txn

    # 2. load the LIVE history (skip anything already folded into a summary)
    msgs = (
        await db.execute(
            select(Message)
            .where(
                Message.conversation_id == convo.id,
                Message.is_summarized == False,  # noqa: E712
            )
            .order_by(Message.created_at)
        )
    ).scalars().all()

    # 3. the memory strategy decides what actually goes to the model
    context = strategy.build_context(msgs, settings.max_context_tokens, convo.summary)

    # 4. call the model
    reply = await provider.chat(context)

    # 5. persist the assistant reply
    asst_msg = Message(
        conversation_id=convo.id,
        role="assistant",
        content=reply,
        token_count=count_tokens(reply),
    )
    db.add(asst_msg)
    await db.commit()

    return ChatResponse(reply=reply, context_messages=len(context))
