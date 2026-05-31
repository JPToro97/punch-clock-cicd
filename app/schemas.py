from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class PunchCreate(BaseModel):
    employee_id: str
    status: Literal["check-in", "break", "check-out"]

class PunchLogResponse(BaseModel):
    id: int
    employee_id: int
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True