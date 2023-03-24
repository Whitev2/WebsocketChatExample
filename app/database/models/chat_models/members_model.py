from sqlalchemy import Column, String, ForeignKey, Integer

from database.postgres import Base


class ChatMember(Base):
    __tablename__ = "chat_members"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(String, nullable=False)

