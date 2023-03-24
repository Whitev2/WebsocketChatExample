from typing import List, Dict

from fastapi import WebSocket
from fastapi import HTTPException, status

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.chat_models.chat_model import Chat
from database.models.chat_models.members_model import ChatMember
from database.models.chat_models.messages_model import Message
from src.schemas.chat_schema import CreateUserRoom, SaveMessage, MessageOut, ChatMemberOut


class ChatCrud:
    def __init__(self, db_session: AsyncSession) -> None:
        self._session: AsyncSession = db_session

    async def _close_session(self):
        if self._session.is_active:
            await self._session.close()

    async def _get_chat_by_id(self, chat_id) -> Chat | None:
        return await self._session.get(Chat, chat_id)

    async def get_chat_history(self, chat_id: int) -> List[MessageOut]:
        chat: Chat = await self._session.get(Chat, chat_id)
        if chat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
        messages = list()
        for message in chat.messages:
            messages.append(MessageOut(**message.__dict__))

        await self._close_session()
        return messages

    async def create_chat(self):
        chat = Chat()
        self._session.add(chat)
        try:
            await self._session.commit()
        except exc.IntegrityError:
            await self._session.rollback()

        return chat.id

    async def create_user_room(self, create_data: CreateUserRoom):
        chat_id = await self.create_chat()
        added_userd = await self.add_user_to_chat([create_data.owner_id], chat_id)

        await self._close_session()
        return added_userd

    async def add_user_to_chat(self, user_id_list: List[str], chat_id: int) -> List[ChatMemberOut]:
        added_users: List[ChatMemberOut] = list()

        if await self._get_chat_by_id(chat_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

        for user_id in user_id_list:
            member = ChatMember(chat_id=chat_id, user_id=user_id)
            self._session.add(member)
            added_users.append(ChatMemberOut(chat_id=chat_id, user_id=user_id))

        try:
            await self._session.commit()
        except exc.IntegrityError:
            await self._session.rollback()
        return added_users

    async def user_in_chat(self, chat_id, user_id):
        chat: Chat = await self._session.get(Chat, chat_id)
        if chat is None:
            return False

        members = [user_id for members in chat.members if user_id == members.user_id]
        if user_id in members:
            return True

    async def save_message(self, message_data: SaveMessage):
        if not await self.user_in_chat(message_data.chat_id, message_data.user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        chat: Chat = await self._session.get(Chat, message_data.chat_id)
        if chat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        message = Message(**message_data.dict())
        chat.messages.append(message)

        try:
            self._session.add(chat)
            await self._session.commit()
        except exc.IntegrityError:
            await self._session.rollback()

        await self._close_session()


class Notifier:
    def __init__(self):
        self.connections: Dict[int, Dict] = dict()

    async def send_in_group(self, chat_id, user_id, message):
        chat_users = self.connections[chat_id]
        for user in chat_users:
            if user != user_id:
                await chat_users[user].send_text(message)

    async def connect(self, chat_id: int, user_id: str, websocket: WebSocket):
        await websocket.accept()

        if self.connections == {} or len(self.connections) == 0:
            self.connections[chat_id] = {}

        if self.connections.get(chat_id, None) is None:
            self.connections[chat_id] = {}

        self.connections[chat_id].update({user_id: websocket})

    def remove(self, chat_id: int, user_id: str):
        try:
            self.connections[chat_id].pop(user_id)

            # delete chat_room
            if len(self.connections[chat_id]) == 0:
                self.connections.pop(chat_id)
        except KeyError:
            pass
