from fastapi import Depends, APIRouter

from db.session import db_dependency
from middleware.auth import get_current_active_admin_user_for_api
from models.auth import User
from models.response import GenericResponse
from service.user import add_new_user, modify_user, remove_user, get_user_data, get_all_user_data

router = APIRouter(
    prefix="/v1/user",
    tags=["User"]
)


@router.post("", response_model=GenericResponse)
async def create_new_user(
    user: User,
    db: db_dependency
) -> GenericResponse:
    result = await add_new_user(user, db)
    return GenericResponse(
        success=True,
        message="User created",
        data=result
    )


@router.put("/{user_name}", response_model=GenericResponse)
async def update_user(
    user_name: str,
    user: User,
    db: db_dependency
) -> GenericResponse:
    result = await modify_user(user_name, user, db)
    return GenericResponse(
        success=True,
        message="User updated",
        data=result
    )


@router.delete("/{user_name}", response_model=GenericResponse)
async def delete_admin_user(
    user_name: str,
    db: db_dependency
) -> GenericResponse:
    _ = await remove_user(db, user_name)
    return GenericResponse(
        success=True,
        message="User deleted",
        data=""
    )


@router.get("/{user_name}", response_model=GenericResponse)
async def get_user(
    user_name: str,
    db: db_dependency
) -> GenericResponse:
    user = await get_user_data(user_name, db)
    return GenericResponse(
        success=True,
        message="User data found",
        data=user
    )


@router.get("", response_model=GenericResponse)
async def get_all_user(
    db: db_dependency
) -> GenericResponse:
    users = await get_all_user_data(db)
    return GenericResponse(
        success=True,
        message="Success",
        data=users
    )
