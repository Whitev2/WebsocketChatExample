from datetime import datetime
import requests
import websockets
import pytest
import uuid

host = "http://localhost:8000/"
ws = 'ws://localhost:8000/ws'



def test_api():

    data_1 = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "stringst"
    }
    data_2 = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "stringst"
    }

    # register
    user_resp = requests.post(f'{host}signup', json=data_1)

    assert user_resp.status_code == 201
    user = user_resp.json()
    user_uid = user.get('uid')
    assert user.get('email') == data_1.get('email')

    # login
    user_resp = requests.post(f'{host}signin', data=data_1)

    assert user_resp.status_code == 200
    login_data = user_resp.json()
    assert login_data.get('token_type') == 'bearer'

    access_token = login_data.get('access_token')

    user_resp = requests.post(f'{host}signin', data=data_2)
    assert user_resp.status_code == 404

    # get user
    user_resp = requests.get(f'{host}user/', headers={'Authorization': 'Bearer ' + access_token})

    assert user_resp.status_code == 200
    user = user_resp.json()
    assert user.get('uid') == user_uid



def test_chat_room():
    data = {
        "owner_id": "1",
    }
    user_resp = requests.post(f'{host}chat/create', json=data)
    assert user_resp.status_code == 201

    user_resp = user_resp.json()

    assert len(user_resp) > 0
    assert user_resp[0].get('chat_id') > 0

    data = {
        "chat_id": "1",
        "users_id": ["2"],
    }
    user_resp = requests.post(f'{host}chat/room/add-user', json=data)
    assert user_resp.status_code == 200

    user_resp = user_resp.json()

    assert len(user_resp) > 0
    assert user_resp[0].get('chat_id') > 0


async def websocket_server():

    async with websockets.connect(ws + '/1/1') as websocket:
        text = 'hello!'

        await websocket.send(text)
        await websocket.close()


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_websocket(anyio_backend):
    async with websockets.connect(ws + '/1/2') as websocket:

        await websocket_server()
        data = await websocket.recv()

        assert data == 'Клиент id: 1 пишет: hello!'

        await websocket.close()