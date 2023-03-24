from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres import get_session
from src.core.oauth2_form import OAuth2PasswordRequestForm
from src.crud.user_crud import UserCrud
from src.schemas.user_schema import UserResponse
from src.schemas.auth_schema import SignUp, Token
from src.schemas.response_schema import Message

router = APIRouter(
    tags=["User Authentication"]
)


@router.post("/signup", status_code=201, responses={201: {"model": UserResponse,
                                                          "description": "User created"},
                                                    409: {"model": Message,
                                                          "description": "User already exist"}})
async def sign_up(signup: SignUp, db_session: AsyncSession = Depends(get_session)):
    user_crud = UserCrud(db_session)
    return await user_crud.create(signup)


@router.post("/signin", response_model=Token, responses={200: {"model": Token,
                                                               "description": "User created"},
                                                         404: {"model": Message,
                                                               "description": "User Not Found"},
                                                         401: {"model": Message,
                                                               "description": "Incorrect email or password"}})
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db_session: AsyncSession = Depends(get_session)):
    user_crud = UserCrud(db_session)
    return await user_crud.validate_user(form_data)
