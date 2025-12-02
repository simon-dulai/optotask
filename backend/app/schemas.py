from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

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
    archived: Optional[bool] = None
    
    # Result fields for task completion
    fields_result: Optional[str] = None
    pressures_result: Optional[str] = None
    scans_result: Optional[str] = None
    
    # Referral tracking
    referral_reason: Optional[str] = None
    referral_sent: Optional[bool] = None
    referral_sent_date: Optional[datetime] = None
    
    # Ticket management
    ticket_status: Optional[str] = None
    completed: Optional[bool] = None
    review_date: Optional[datetime] = None
    closed_date: Optional[datetime] = None


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

    # NEW: Result fields
    fields_result: Optional[str] = None
    pressures_result: Optional[str] = None
    scans_result: Optional[str] = None

    # NEW: Referral tracking
    referral_reason: Optional[str] = None
    referral_sent: bool = False
    referral_sent_date: Optional[datetime] = None

    # NEW: Ticket management
    ticket_status: str = "open"
    completed: bool = False
    review_date: Optional[datetime] = None
    closed_date: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Lets Pydantic read from SQLAlchemy models

# NEW SCHEMAS FOR TICKET MANAGEMENT
# ============================================

class PostponeTicket(BaseModel):
    """Schema for postponing a ticket to a new date"""
    review_date: datetime


class UpdateWithResults(BaseModel):
    """Schema for updating task with results/outcomes"""
    fields_result: Optional[str] = None  # e.g., "All clear" or "Needs glaucoma referral"
    pressures_result: Optional[str] = None  # e.g., "IOP 16mmHg normal" or "IOP 28mmHg elevated"
    scans_result: Optional[str] = None  # e.g., "OCT normal" or "Glaucoma suspect"
    referral_reason: Optional[str] = None  # e.g., "High IOP, glaucoma suspect"

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
