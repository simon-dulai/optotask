import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, Boolean, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship  # Not from .ext.declarative
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum



Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, index=True, nullable=False)
    email = Column(Text, unique=True, index=True, nullable=False)
    hashed_password = Column(Text, nullable=False)

    # Relationship to patients
    patients = relationship("Patient", back_populates="owner")

class Patient(Base):
    __tablename__ = "Patients"
    idx = Column("ID No.", Integer, primary_key = True)
    initial = Column("Initials", Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    fields = Column("Fields", Boolean, default = False)
    fields_result = Column(Text, nullable=True)  # NEW: "All clear" or "Needs glaucoma referral"


    pressures = Column("IOP", Boolean, default = False)
    pressures_result = Column(Text, nullable=True)  # NEW: Result notes


    scans = Column("Photos/OCT", Boolean, default = False)
    scans_result = Column(Text, nullable=True)  # NEW: Result notes


    referral = Column ("Referral", Boolean, default = False)
    referral_reason = Column(Text, nullable=True)  # NEW: Why referral needed
    referral_sent = Column(Boolean, default=False)  # NEW: Has referral been sent?
    referral_sent_date = Column(DateTime, nullable=True)  # NEW: When sent

    ticket_status = Column(String, default="open")  # NEW: "open", "closed"
    completed = Column(Boolean, default=False)  # NEW: All tasks done?
    review_date = Column(DateTime, nullable=True)  # NEW: When to show this ticket (for postponing)
    closed_date = Column(DateTime, nullable=True)  # NEW: When ticket was closed

    notes = Column("Additional Notes", Text, nullable=True)


    archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Bonus: timestamps!

    # Foreign key to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    archived = Column(Boolean, default=False)  # For permanent archive

    # Relationship to user
    owner = relationship("User", back_populates="patients")


    def __repr__(self):
        return f"<Patient {self.idx}: {self.initial} - Status: {self.ticket_status}>"

import os

db_path= os.getenv("DATABASE_URL", "optotask.db")
engine = create_engine(f"sqlite:///{db_path}", echo=True)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()