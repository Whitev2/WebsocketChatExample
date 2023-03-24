from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres import get_session
from src.crud.chat_crud import ChatCrud
from src.schemas.chat_schema import CreateUserRoom, MessageOut

router = APIRouter(prefix='/chat')


@router.post("/create")
async def create_chat_room(create_data: CreateUserRoom,
                           db_session: AsyncSession = Depends(get_session)):
    chat_crud = ChatCrud(db_session)
    return await chat_crud.create_user_room(create_data)


@router.get("/history")
async def get_chat_history(chat_id: int,
                           db_session: AsyncSession = Depends(get_session)):
    chat_crud = ChatCrud(db_session)
    return await chat_crud.get_chat_history(chat_id)