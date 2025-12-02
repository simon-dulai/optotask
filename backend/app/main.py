from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta
from typing import List
import os

from .database import get_db, Patient, User
from .schemas import (
    TaskCreate, TaskUpdate, TaskResponse,
    UserCreate, UserLogin, Token, UserResponse
)
from .auth import (
    verify_password, get_password_hash, create_access_token,
    SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(title="OptoTask API")

# CORS railway
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://optotask.up.railway.app", "http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "OptoTask API is running"}
#User points
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get the current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


#Login points

@app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account"""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # if email exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Find by username
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


#Task Points (login first)

@app.post("/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
        task: TaskCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # Added auth
):

    existing = db.query(Patient).filter(
        Patient.idx == task.idx,
        Patient.user_id == current_user.id  # filter by user
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Patient {task.idx} already exists"
        )

    new_patient = Patient(
        idx=task.idx,
        initial=task.initial,
        fields=task.fields,
        pressures=task.pressures,
        scans=task.scans,
        referral=task.referral,
        notes=task.notes,
        user_id=current_user.id  # link to current user
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@app.get("/read/{patient_id}", response_model=TaskResponse)
def read_task(
        patient_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # FIXED: Added auth
):

    patient = db.query(Patient).filter(
        Patient.idx == patient_id,
        Patient.user_id == current_user.id,  # filter by user
        Patient.archived == False
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return patient


@app.get("/read_archive", response_model=List[TaskResponse])
def get_archived_tasks(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # Auth
):

    archived_patients = db.query(Patient).filter(
        Patient.user_id == current_user.id,
        Patient.archived == True
    ).all()

    return archived_patients


@app.get("/see_all", response_model=List[TaskResponse])
def get_all_tasks(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    tasks = db.query(Patient).filter(
        Patient.user_id == current_user.id,
        Patient.archived == False
    ).all()

    return tasks

@app.get("/tickets/open", response_model=List[TaskResponse])
def get_open_tickets(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    tickets = db.query(Patient).filter(
        Patient.user_id == current_user.id,
        Patient.ticket_status == "open",
        Patient.archived == False
    ).all()

    return tickets

@app.put("/update/{patient_id}", response_model=TaskResponse)
def update_task(
        patient_id: int,
        task_update: TaskUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    patient = db.query(Patient).filter(
        Patient.idx == patient_id,
        Patient.user_id == current_user.id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Update only provided fields
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    return patient


@app.delete("/tasks/{patient_id}", status_code=status.HTTP_200_OK)
def archive_task(
        patient_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    #archive
    patient = db.query(Patient).filter(
        Patient.idx == patient_id,
        Patient.user_id == current_user.id  # FIXED: Filter by user
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    patient.archived = True
    db.commit()

    return {"message": f"Patient {patient_id} archived successfully"}

@app.get("/search_archive/{patient_id}", response_model=TaskResponse)
def search_archive(
        patient_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    patient = db.query(Patient).filter(
        Patient.idx == patient_id,
        Patient.user_id == current_user.id,
        Patient.archived == True  # Only  archived patients
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found in archive"
        )

    return patient


#endpoint

@app.get("/")
def root():

    return {"message": "Welcome to OptoTask API! Go to /docs for API documentation"}