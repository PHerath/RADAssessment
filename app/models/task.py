from datetime import datetime

from pydantic import BaseModel


class TaskModel(BaseModel):
    name: str
    type: str
    description: str


class CreateTaskResponse(BaseModel):
    id: int
    name: str
    type: str
    description: str
    create_date: datetime
    update_date: datetime

    class Config:
        from_attributes = True
