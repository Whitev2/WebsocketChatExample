from sqlalchemy import Column, TIMESTAMP, BOOLEAN, Integer, text
from sqlalchemy.orm import relationship
from typing import List

from database.models.chat_models.members_model import ChatMember
from database.models.chat_models.messages_model import Message
from database.postgres import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    is_active = Column(BOOLEAN, default=True)

    members: List[ChatMember] = relationship(
        "ChatMember",
        cascade="all, delete-orphan", lazy='joined'
    )
    messages: List[Message] = relationship(
        "Message",
        cascade="all, delete-orphan", lazy='joined'
    )

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


