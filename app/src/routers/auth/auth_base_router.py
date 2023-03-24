from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres import get_session
from src.core.oauth2 import JWTBearer
from src.crud.user_crud import UserCrud


router = APIRouter(
    tags=["Base Authentication"]
)


@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(token: str = Depends(JWTBearer()),
                 db_session: AsyncSession = Depends(get_session)
                 ):
    """
    Выход из системы и блокировка токенов на время их действия
    """

    user_crud: UserCrud = UserCrud(db_session)
    return await user_crud.logout(token)
