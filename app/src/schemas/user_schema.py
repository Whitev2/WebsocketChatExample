from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    uid: str
    email: EmailStr


class UserResponse(UserBase):
    pass
