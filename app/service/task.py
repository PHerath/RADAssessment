import datetime

from crud.task import create, get, update, delete, get_all
from db.models import Task
from exception.exception import NoDataFoundException
from models.task import TaskModel, CreateTaskResponse, UpdateTaskModel


async def create_new_task(task: TaskModel, db):
    _task = Task(name=task.name, type=task.type, description=task.description)
    created_task = await create(_task, db)
    return CreateTaskResponse.model_validate(created_task)


async def get_all_task(db):
    _task_list = await get_all(db)
    task_list = [CreateTaskResponse.model_validate(_task) for _task in _task_list]
    return task_list


async def get_task(task_id: int, db):
    _task = await get(task_id, db)
    if not _task:
        raise NoDataFoundException("Task not found")
    return CreateTaskResponse.model_validate(_task)


async def modify_task(task_id: int, task: UpdateTaskModel, db):
    existing_task = await get(task_id, db)
    if not existing_task:
        raise NoDataFoundException("Task not found")
    if task.type:
        existing_task.type = task.type
    if task.description:
        existing_task.description = task.description
    existing_task.update_date = datetime.datetime.now()
    updated_task = await update(existing_task, db)
    if not updated_task:
        raise NoDataFoundException("Task not found")
    return CreateTaskResponse.model_validate(updated_task)


async def remove_task(task_id: int, db):
    _ = await delete(task_id, db)
    return True
