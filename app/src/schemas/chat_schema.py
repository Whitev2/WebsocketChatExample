from datetime import datetime
from typing import List, Union

from pydantic.main import BaseModel


class CreateUserRoom(BaseModel):
    owner_id: str


class AddUserToChat(BaseModel):
    chat_id: int
    users_id: List[Union[str, int]]


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
