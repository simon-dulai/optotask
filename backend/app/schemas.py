from pydantic import BaseModel, EmailStr
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
    archived: bool = False


class TaskUpdate(BaseModel):
    """Schema for updating a task - all fields optional"""
    initial: Optional[str] = None
    fields: Optional[bool] = None
    pressures: Optional[bool] = None
    scans: Optional[bool] = None
    referral: Optional[bool] = None
    notes: Optional[str] = None
    archived: Optional[bool] = None  # FIXED: Added Optional type


class TaskResponse(BaseModel):
    """Schema for task responses from API"""
    idx: int
    initial: str
    fields: bool
    pressures: bool
    scans: bool
    referral: bool
    notes: Optional[str]
    archived: bool
    user_id: int  # FIXED: Added user_id field

    class Config:
        from_attributes = True  # Lets Pydantic read from SQLAlchemy models


# ============================================
# USER AUTHENTICATION SCHEMAS
# ============================================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True