import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from config.config import SECRET_KEY, ALGORITHM
from crud.user import get_user
from db.models import UserInDB
from db.session import get_db_session
from exception.exception import UnauthorizedException
from service.user import user_roles
from util.util import verify_password

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_user_by_user_name(db, user_name: str) -> Optional[UserInDB]:
    user = await get_user(user_name, db)
    return user


async def authenticate_user(db, username: str, password: str) -> Optional[UserInDB]:
    user = await get_user_by_user_name(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            logger.error("Could not validate credentials: User name not found")
            raise UnauthorizedException()
    except InvalidTokenError as e:
        logger.error(f"Could not validate credentials: {e}")
        raise UnauthorizedException()
    user = await get_user_by_user_name(get_db_session(), username)
    if user is None:
        logger.error("Could not validate credentials: user not found in db")
        raise UnauthorizedException()
    if user.role.role_name != role:
        logger.error("Could not validate credentials: user role does not match")
        raise UnauthorizedException()
    return user


async def get_current_active_user(current_user: Annotated[UserInDB, Depends(get_current_user)]) -> UserInDB:
    if current_user.disabled:
        logger.warning("Inactive user")
        raise UnauthorizedException()
    return current_user


async def get_current_active_admin_user_for_api(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
):
    if current_user.role.role_name != "admin":
        logger.warning("Only admins can perform this action")
        raise UnauthorizedException()
    return current_user


async def get_current_active_user_for_api(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
):
    existing_user_roles = await user_roles(get_db_session())
    if current_user.role.role_name not in existing_user_roles:
        logger.warning("Unauthorized access")
        raise UnauthorizedException()
    return current_user
