from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ConversationCreate(BaseModel):
    title: str = "New conversation"


class ConversationOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    token_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    content: str


class ChatResponse(BaseModel):
    reply: str
    context_messages: int  # how many messages the strategy actually sent to the model
