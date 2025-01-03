from fastapi import HTTPException, Depends, status, APIRouter
from typing import List, Annotated

from crud.user import create_user, update_user, delete_user, get_user
from db.models import UserInDB
from middleware.auth import get_current_active_user, fake_users_db
from models.auth import User

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


async def get_current_active_admin_user(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action",
        )
    return current_user


# User Management APIs (admin-only)
@router.post("")
async def create_admin_user(
    user: UserInDB,
    current_user: Annotated[UserInDB, Depends(get_current_active_admin_user)],
):
    await create_user(user)
    return {"msg": "User created successfully"}


@router.put("/{username}")
async def update_admin_user(
    user_name: str,
    user: User,
    current_user: Annotated[UserInDB, Depends(get_current_active_admin_user)],
    db
):
    await update_user(db, user_name)
    return {"msg": "User updated successfully"}


@router.delete("/{username}")
async def delete_admin_user(
    user_name: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_admin_user)],
    db
):
    await delete_user(db, user_name)
    return {"msg": "User deleted successfully"}


@router.get("/{username}", response_model=User)
async def get_admin_user(
    username: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_admin_user)],
    db
):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
