from fastapi import APIRouter, Depends

from api.auth import router as auth_router
from api.task import router as task_router
from api.user import router as user_router
from middleware.auth import get_current_active_admin_user_for_api, get_current_active_user_for_api

api_admin_routers = APIRouter(
    dependencies=[Depends(get_current_active_admin_user_for_api)]
)
api_routers = APIRouter(
    dependencies=[Depends(get_current_active_user_for_api)]
)
auth_routers = APIRouter()


api_routers.include_router(task_router)
api_admin_routers.include_router(user_router)
auth_routers.include_router(auth_router)
