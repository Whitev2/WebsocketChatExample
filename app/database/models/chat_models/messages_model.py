from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Integer, text

from database.postgres import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(String, nullable=False)

    body = Column(String)
    type = Column(String)
    content = Column(String)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
