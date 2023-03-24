from __future__ import annotations

from pydantic import constr
from pydantic import BaseModel, EmailStr


class SignUp(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)


class SignIn(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)


class Token(BaseModel):
    refresh_token: str
    access_token: str
    access_time: int
    token_type: str = 'bearer'


class Logout(BaseModel):
    refresh_token: str

