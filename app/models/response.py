from typing import Any, Optional
from pydantic import BaseModel


class GenericResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
