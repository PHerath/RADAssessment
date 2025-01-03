import logging

from db.models import UserInDB
from exception.exception import CrudException

logger = logging.getLogger(__name__)


async def get_user(db, user_name: str):
    exist_user = db.query(UserInDB).filter(UserInDB.user_name == user_name).one_or_none()
    if not exist_user:
        logger.warning(f"User does not exist")
        return None
    return exist_user


async def create_user(db, user: UserInDB):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user(db, user: UserInDB):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def delete_user(db, username: str):
    if username in db:
        del db[username]