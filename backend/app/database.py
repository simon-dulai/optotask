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
    fields = Column("Fields", Boolean, default = False)
    pressures = Column("IOP", Boolean, default = False)
    scans = Column("Photos/OCT", Boolean, default = False)
    referral = Column ("Referral", Boolean, default = False)
    notes = Column("Additional Notes", Text, nullable=True)
    archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Bonus: timestamps!

    # Foreign key to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to user
    owner = relationship("User", back_populates="patients")


    def __repr__(self):
        return f"{self.idx} {self.initial} { self.fields} { self.pressures} {self.scans}  {self.referral} { self.notes}"


engine = create_engine("sqlite:///optotask.db", echo=True)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()