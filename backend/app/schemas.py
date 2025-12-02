from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):

    idx: int  #customer number
    initial: str
    fields: bool = False
    pressures: bool = False
    scans: bool = False
    referral: bool = False
    notes: Optional[str] = None
    archived: bool = False


class TaskUpdate(BaseModel):

    initial: Optional[str] = None
    fields: Optional[bool] = None
    pressures: Optional[bool] = None
    scans: Optional[bool] = None
    referral: Optional[bool] = None
    notes: Optional[str] = None
    archived: Optional[bool] = None
    
    # fields
    fields_result: Optional[str] = None
    pressures_result: Optional[str] = None
    scans_result: Optional[str] = None
    
    # referral
    referral_reason: Optional[str] = None
    referral_sent: Optional[bool] = None
    referral_sent_date: Optional[datetime] = None
    
    # ticket system
    ticket_status: Optional[str] = None
    completed: Optional[bool] = None
    review_date: Optional[datetime] = None
    closed_date: Optional[datetime] = None


class TaskResponse(BaseModel):

    idx: int
    initial: str
    fields: bool
    pressures: bool
    scans: bool
    referral: bool
    notes: Optional[str]
    archived: bool
    user_id: int


    fields_result: Optional[str] = None
    pressures_result: Optional[str] = None
    scans_result: Optional[str] = None


    referral_reason: Optional[str] = None
    referral_sent: bool = False
    referral_sent_date: Optional[datetime] = None


    ticket_status: str = "open"
    completed: bool = False
    review_date: Optional[datetime] = None
    closed_date: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Lets Pydantic read from SQLAlchemy models

# New Ticket Management

class PostponeTicket(BaseModel):

    review_date: datetime


class UpdateWithResults(BaseModel):
    """Schema for updating task with results/outcomes"""
    fields_result: Optional[str] = None  # e.g., "All clear" or "Needs glaucoma referral"
    pressures_result: Optional[str] = None  # e.g., "IOP 16mmHg normal" or "IOP 28mmHg elevated"
    scans_result: Optional[str] = None  # e.g., "OCT normal" or "Glaucoma suspect"
    referral_reason: Optional[str] = None  # e.g., "High IOP, glaucoma suspect"

#User Auth

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
