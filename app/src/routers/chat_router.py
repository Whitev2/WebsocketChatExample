from pydantic.typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres import get_session
from src.crud.chat_crud import ChatCrud
from src.schemas.chat_schema import CreateUserRoom, MessageOut, AddUserToChat, ChatMemberOut
from src.schemas.response_schema import Message

router = APIRouter(prefix='/chat')


@router.post("/create", status_code=201,
             response_model=List[ChatMemberOut])
async def create_chat_room(create_data: CreateUserRoom,
                           db_session: AsyncSession = Depends(get_session)):
    """
    Создание чата с одним владельцем

    owner_id: str/int
    """
    chat_crud = ChatCrud(db_session)
    return await chat_crud.create_user_room(create_data)


@router.post("/room/add-user",
             response_model=List[ChatMemberOut],
             responses={404: {"model": Message,
                              "description": "Chat not found"}})
async def add_user_to_room(create_data: AddUserToChat,
                           db_session: AsyncSession = Depends(get_session)):
    """
    Массовое добавление пользователей в чат

    chat_id: int
    user_id: str/int
    """
    chat_crud = ChatCrud(db_session)
    return await chat_crud.add_user_to_chat(create_data.users_id, create_data.chat_id)


@router.get("/history",
            response_model=List[MessageOut],
            responses={404: {"model": Message,
                             "description": "Chat not found"}
                       })
async def get_chat_history(chat_id: int, db_session: AsyncSession = Depends(get_session)):
    """
    Получение истории из чата

    chat_id: int
    """
    chat_crud = ChatCrud(db_session)
    return await chat_crud.get_chat_history(chat_id)
