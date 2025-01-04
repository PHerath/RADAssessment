from fastapi import APIRouter
from api.task import router as task_router
from api.user import router as user_router


api_routers = APIRouter()


api_routers.include_router(task_router)
api_routers.include_router(user_router)
