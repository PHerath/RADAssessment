import logging

from sqlalchemy.exc import SQLAlchemyError

from db.models import UserInDB, Role
from exception.exception import CrudException

logger = logging.getLogger(__name__)


async def get_all_users(db):
    try:
        users = db.query(UserInDB).all()
        return users
    except SQLAlchemyError as e:
        logger.error(f"An error occurred while fetching user data in the database: {e}")
        raise CrudException("Unable to get the user data due to a database error.")


async def get_user(user_name: str, db):
    try:
        exist_user = db.query(UserInDB).filter(UserInDB.user_name == user_name).one_or_none()
        if not exist_user:
            logger.warning("User does not exist")
            return None
        return exist_user
    except SQLAlchemyError as e:
        logger.error("An error occurred while fetching user data in the database.", exc_info=e)
        raise CrudException("Unable to get the user data due to a database error.")


async def create_user(user: UserInDB, db):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        logger.error("An error occurred while adding a user in the database.", exc_info=e)
        raise CrudException("Unable to add user data due to a database error.")


async def update_user(user: UserInDB, db):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        logger.error("An error occurred while updating a user in the database.", exc_info=e)
        db.roleback()
        raise CrudException("Unable to modify user data due to a database error.")


async def delete_user(user_name: str, db):
    try:
        user = db.query(UserInDB).filter(UserInDB.id == user_name).first()
        if not user:
            raise CrudException("Not found task for given id")
        db.delete(user)
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error("An error occurred while deleting a user in the database.", exc_info=e)
        db.roleback()
        raise CrudException("Unable to remove user data due to a database error.")


async def get_user_role(role: str, db):
    try:
        exist_role = db.query(Role).filter(Role.role_name == role).one_or_none()
        if not exist_role:
            logger.warning("Role does not exist")
            return None
        return exist_role
    except SQLAlchemyError as e:
        logger.error("An error occurred while fetching user data in the database.", exc_info=e)
        raise CrudException("Unable to get the user data due to a database error.")


async def get_user_roles(db):
    try:
        exist_user_roles = db.query(Role).all()
        return exist_user_roles
    except SQLAlchemyError as e:
        logger.error("An error occurred while fetching user data in the database.", exc_info=e)
        raise CrudException("Unable to get the user data due to a database error.")
