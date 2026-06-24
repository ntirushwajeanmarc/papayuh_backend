from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import Training, TrainingRegistration

router = APIRouter(prefix="/youth", tags=["Youth Hub"])

class TrainingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    instructor: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    capacity: Optional[int] = None
    location: Optional[str] = None

class RegistrationCreate(BaseModel):
    training_id: int
    citizen_id: int

@router.get("/trainings/")
def list_trainings(db: Session = Depends(get_db)):
    return db.query(Training).all()

@router.post("/trainings/", status_code=201)
def create_training(data: TrainingCreate, db: Session = Depends(get_db)):
    t = Training(**data.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.post("/registrations/", status_code=201)
def register(data: RegistrationCreate, db: Session = Depends(get_db)):
    reg = TrainingRegistration(**data.model_dump())
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return reg
