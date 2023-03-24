from sqlalchemy import Column, String, TIMESTAMP, BOOLEAN, Integer, text
from database.postgres import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, unique=True)
    email = Column(String, unique=True)
    hash_password = Column(String)

    is_active = Column(BOOLEAN, default=True)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))