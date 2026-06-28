from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models import User
from app.schemas import Token, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(body: UserCreate, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(select(User).where(User.username == body.username))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username taken")
    user = User(username=body.username, hashed_password=hash_password(body.password))
    db.add(user)
    await db.commit()
    return Token(access_token=create_access_token(user.username))


@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.username == form.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Bad credentials")
    return Token(access_token=create_access_token(user.username))
