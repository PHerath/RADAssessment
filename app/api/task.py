from fastapi import APIRouter, Depends

from db.session import db_dependency
from middleware.auth import get_current_active_user_for_api
from models.response import GenericResponse
from models.task import TaskModel
from service.task import create_new_task, modify_task, get_task, remove_task, get_all_task

router = APIRouter(
    prefix="/v1/task",
    tags=["Task"]
)


@router.get("", response_model=GenericResponse)
async def get_all(db: db_dependency):
    result = await get_all_task(db)
    return GenericResponse(
        success=True,
        message="Task list received",
        data=result
    )


@router.get("/{task_id}", response_model=GenericResponse)
async def get_one(task_id: int, db: db_dependency):
    result = await get_task(task_id, db)
    return GenericResponse(
        success=True,
        message="Task Found",
        data=result
    )


@router.post("", response_model=GenericResponse)
async def add_new_task(task: TaskModel, db: db_dependency):
    result = await create_new_task(task, db)
    return GenericResponse(
        success=True,
        message="Task added",
        data=result
    )


@router.put("/{task_id}", response_model=GenericResponse)
async def modify(task_id: int, task: TaskModel, db: db_dependency):
    result = await modify_task(task_id, task, db)
    return GenericResponse(
        success=True,
        message="Task updated",
        data=result
    )


@router.delete("/{task_id}", response_model=GenericResponse)
async def remove(task_id: int, db: db_dependency):
    _ = await remove_task(task_id, db)
    return GenericResponse(
        success=True,
        message="Task deleted"
    )
