import datetime
import logging

from crud.user import get_user, create_user, update_user, delete_user, get_user_role, get_all_users, get_user_roles
from db.models import UserInDB
from exception.exception import NoDataFoundException, BadRequestException
from models.auth import User, CreateUserResponse
from util.util import get_password_hash

logger = logging.getLogger(__name__)


async def add_new_user(user: User, db):
    if user.password != user.confirm_password:
        logger.warning("password and confirm password not matching")
        raise BadRequestException("password and confirm password should match")
    role = await get_user_role(user.role, db)
    if not role:
        raise NoDataFoundException("Role does not exist")
    hashed_pwd = get_password_hash(user.password)
    _user = UserInDB(
        user_name=user.user_name,
        email=user.email,
        hashed_password=hashed_pwd,
        role_id=role.id
    )
    created_user = await create_user(_user, db)
    return CreateUserResponse.model_validate(created_user)


async def get_all_user_data(db):
    users = await get_all_users(db)
    list_of_users = [CreateUserResponse.model_validate(_user) for _user in users]
    return list_of_users


async def get_user_data(user_name: str, db):
    _user = await get_user(user_name, db)
    if not _user:
        logger.warning("user not found in db")
        raise NoDataFoundException("user not found")
    return CreateUserResponse.model_validate(_user)


async def modify_user(user_name: str, user: User, db):
    existing_user = await get_user(user_name, db)
    if not existing_user:
        logger.warning("user not found in db")
        raise NoDataFoundException("user not found")
    if user.user_name:
        existing_user.user_name = user.user_name
    if user.password:
        existing_user.password = user.password
    existing_user.update_date = datetime.datetime.now()
    updated_user = await update_user(existing_user, db)
    return CreateUserResponse.model_validate(updated_user)


async def remove_user(user_name: str, db):
    _ = await delete_user(user_name, db)
    return True


async def user_roles(db):
    _user_roles = await get_user_roles(db)
    _roles = [user_role.role_name for user_role in _user_roles]
    return _roles
