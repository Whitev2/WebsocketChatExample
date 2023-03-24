from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.postgres import Postgres
from database.redis import RedRedis
from src.routers import user_router, chat_router
from src.routers.auth import auth_user
from src.routers.chat_ws import ws

config_path = Path('src/loggeri/logging_config.json')


def init_app():
    app = FastAPI(
        title="Web socket app",
        description="Handling Our Users",
        version="1",
        debug=False
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        await Postgres().connect_to_storage()
        await RedRedis().connect_to_storage()

    @app.on_event("shutdown")
    async def shutdown():
        pass

    app.include_router(auth_user.router)
    app.include_router(user_router.router)
    app.include_router(chat_router.router)

    app.mount('/ws', ws)
    return app


app = init_app()
