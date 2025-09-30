from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    idx: int  # Patient ID/customer number
    initial: str
    fields: bool = False
    pressures: bool = False
    scans: bool = False
    referral: bool = False
    notes: Optional[str] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task - all fields optional"""
    initial: Optional[str] = None
    fields: Optional[bool] = None
    pressures: Optional[bool] = None
    scans: Optional[bool] = None
    referral: Optional[bool] = None
    notes: Optional[str] = None


class TaskResponse(BaseModel):
    """Schema for task responses from API"""
    idx: int
    initial: str
    fields: bool
    pressures: bool
    scans: bool
    referral: bool
    notes: Optional[str]

    class Config:
        from_attributes = True  # Lets Pydantic read from SQLAlchemy models