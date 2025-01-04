from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    user_name: str
    email: str
    password: str
    confirm_password: str
    role: str


class CreateUserResponse(BaseModel):
    user_name: str
    email: str

    class Config:
        from_attributes = True


# class UserInDB(User):
#     hashed_password: str
