from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres import get_session
from src.crud.user_crud import UserCrud
from src.routers.dopends import JWTValidateUser, current_user
from src.schemas.user_schema import UserResponse

router = APIRouter(prefix='/user')


@router.get("/", response_model=UserResponse)
async def get_user(db_session: AsyncSession = Depends(get_session), user_data: JWTValidateUser = Depends(current_user)):
    user_crud: UserCrud = UserCrud(db_session)
    return await user_crud.get_user(user_id=user_data.user_id)