from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import auth_router, chat, conversations


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Chatting Bot - Stateful Chat API", lifespan=lifespan)
app.include_router(auth_router.router)
app.include_router(conversations.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "chatting-bot"}
