import asyncio

from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets import exceptions as ws_exc

from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres import get_session
from src.crud.chat_crud import Notifier, ChatCrud
from src.schemas.chat_schema import SaveMessage

ws = FastAPI()

ws.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

notifier = Notifier()


@ws.websocket("/{chat_id}/{user_id}")
async def websocket_endpoint(chat_id: int,
                             user_id: str,
                             websocket: WebSocket,
                             db_session: AsyncSession = Depends(get_session)):
    chat_crud = ChatCrud(db_session)
    if not await chat_crud.user_in_chat(chat_id, user_id):
        raise ws_exc.InvalidParameterValue(name='user_id', value=user_id)

    await notifier.connect(chat_id, user_id, websocket)
    row = f"Клиент id: {user_id} пишет: "

    try:
        while True:
            data = await websocket.receive_text()

            asyncio.create_task(chat_crud.save_message(SaveMessage(chat_id=chat_id,
                                                                   user_id=str(user_id),
                                                                   body=data,
                                                                   type='text',
                                                                   content='')))  # for background task

            await notifier.send_in_group(chat_id, user_id, row + data)
    except WebSocketDisconnect:
        notifier.remove(chat_id, user_id)
