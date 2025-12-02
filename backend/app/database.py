import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, index=True, nullable=False)
    email = Column(Text, unique=True, index=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    patients = relationship("Patient", back_populates="owner")

class Patient(Base):
    __tablename__ = "Patients"
    idx = Column("ID No.", Integer, primary_key=True)
    initial = Column("Initials", Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    fields = Column("Fields", Boolean, default=False)
    fields_result = Column(Text, nullable=True)

    pressures = Column("IOP", Boolean, default=False)
    pressures_result = Column(Text, nullable=True)

    scans = Column("Photos/OCT", Boolean, default=False)
    scans_result = Column(Text, nullable=True)

    referral = Column("Referral", Boolean, default=False)
    referral_reason = Column(Text, nullable=True)
    referral_sent = Column(Boolean, default=False)
    referral_sent_date = Column(DateTime, nullable=True)

    ticket_status = Column(String, default="open")
    completed = Column(Boolean, default=False)
    review_date = Column(DateTime, nullable=True)
    closed_date = Column(DateTime, nullable=True)

    notes = Column("Additional Notes", Text, nullable=True)
    archived = Column(Boolean, default=False)

    owner = relationship("User", back_populates="patients")

    def __repr__(self):
        return f"<Patient {self.idx}: {self.initial} - Status: {self.ticket_status}>"

# Database configuration for Railway2
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Railway PostgreSQL - ensure we're using psycopg driver
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    # For local development - fallback to SQLite
    DATABASE_URL = "sqlite:///./optotask.db"

print(f"Connecting to database: {DATABASE_URL.split('@')[0]}@****")  # Log connection (hide password)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
