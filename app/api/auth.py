from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from db.session import db_dependency
from middleware.auth import authenticate_user, create_access_token
from models.auth import Token

router = APIRouter(
    prefix="",
    tags=["Auth"]
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.user_name, "email": user.email, "role": user.role.role_name},
        expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
