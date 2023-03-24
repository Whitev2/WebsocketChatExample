from datetime import datetime

from pydantic.main import BaseModel


class CreateUserRoom(BaseModel):
    owner_id: str


class SaveMessage(BaseModel):
    chat_id: int
    user_id: str

    body: str
    type: str
    content: str


class MessageOut(BaseModel):
    id: int

    chat_id: int
    user_id: str

    body: str
    type: str
    content: str

    created_at: datetime


class ChatOut(BaseModel):
    chat_id: int
