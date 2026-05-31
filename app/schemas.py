from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class PunchCreate(BaseModel):
    badge_number: str
    status: Literal["check-in", "break", "check-out"]

class PunchLogResponse(BaseModel):
    id: int
    employee_id: int
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True

class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, pattern="^[A-Za-z\s]+$")
    badge_number: str = Field(..., pattern="^\d+$")

class EmployeeResponse(BaseModel):
    id: int
    name: str
    badge_number: str

    class Config:
        from_attributes = True