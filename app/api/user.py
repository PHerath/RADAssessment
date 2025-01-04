from fastapi import HTTPException, Depends, status, APIRouter
from typing import List, Annotated

from crud.user import create_user, update_user, delete_user, get_user
from db.models import UserInDB
from db.session import db_dependency
from middleware.auth import get_current_active_user, fake_users_db
from models.auth import User
from models.response import GenericResponse
from service.user import add_new_user, modify_user, remove_user

router = APIRouter(
    prefix="/v1/user",
    tags=["User"]
)


# async def get_current_active_admin_user(
#     current_user: Annotated[UserInDB, Depends(get_current_active_user)],
# ):
#     if current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only admins can perform this action",
#         )
#     return current_user


# User Management APIs (admin-only)
@router.post("", response_model=GenericResponse)
async def create_new_user(
    user: User,
    # current_user: Annotated[UserInDB, Depends(get_current_active_admin_user)],
    db: db_dependency
):
    result = await add_new_user(user, db)
    return GenericResponse(
        success=True,
        message="User created",
        data=result
    )


@router.put("/{username}", response_model=GenericResponse)
async def update_user(
    user_name: str,
    # user: User,
    # current_user: Annotated[UserInDB, Depends(get_current_active_admin_user)],
    db: db_dependency
):
    await modify_user(db, user_name)
    return {"msg": "User updated successfully"}


@router.delete("/{username}", response_model=GenericResponse)
async def delete_admin_user(
    user_name: str,
    # current_user: Annotated[UserInDB, Depends(get_current_active_admin_user)],
    db: db_dependency
):
    await remove_user(db, user_name)
    return {"msg": "User deleted successfully"}


@router.get("/{user_name}", response_model=GenericResponse)
async def get_admin_user(
    user_name: str,
    # current_user: Annotated[UserInDB, Depends(get_current_active_admin_user)],
    db: db_dependency
):
    user = get_user(db, user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return GenericResponse(
        succcess=True,
        message="User data found",
        data=user
    )
