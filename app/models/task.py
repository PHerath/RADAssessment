from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskModel(BaseModel):
    name: str
    type: Optional[str]
    description: Optional[str]


class UpdateTaskModel(BaseModel):
    type: Optional[str]
    description: Optional[str]


class CreateTaskResponse(BaseModel):
    id: int
    name: str
    type: str
    description: str
    create_date: datetime
    update_date: datetime

    class Config:
        from_attributes = True
