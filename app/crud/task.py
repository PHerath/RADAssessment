import logging

from sqlalchemy.exc import SQLAlchemyError

from db.models import Task
from exception.exception import CrudException

logger = logging.getLogger(__name__)


async def create(task: Task, db):
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as e:
        logger.error("An error occurred while creating a task in the database.", exc_info=e)
        raise CrudException("Unable to create the task due to a database error.")


async def get_all(db):
    try:
        task = db.query(Task).all()
        return task
    except SQLAlchemyError as e:
        logger.error(e)
        raise CrudException(f"Unable to get the tasks due to a database error: {e}")


async def get(task_id: int, db):
    try:
        task = db.query(Task).filter(Task.id == task_id).one_or_none()
        return task
    except SQLAlchemyError as e:
        logger.error(e)
        raise CrudException(f"Unable to get the task due to a database error: {e}")


async def update(task: Task, db):
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as e:
        logger.error("An error occurred while updating the task in the database.", exc_info=e)
        db.rollback()
        raise CrudException("Unable to update the task due to a database error.")


async def delete(task_id: int, db):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise CrudException("Not found task for given id")
        db.delete(task)
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Error deleting task: {str(e)}")
        db.rollback()
        raise CrudException(f"Failed to remove task {str(e)}")
