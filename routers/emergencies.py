from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import EmergencyAlert

router = APIRouter(prefix="/emergencies", tags=["Emergency Alerts"])

class AlertCreate(BaseModel):
    alert_type: str
    title: str
    description: Optional[str] = None
    severity: Optional[str] = "Medium"
    location: Optional[str] = None

@router.get("/")
def list_alerts(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    return db.query(EmergencyAlert).order_by(EmergencyAlert.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/", status_code=201)
def create_alert(data: AlertCreate, db: Session = Depends(get_db)):
    alert = EmergencyAlert(**data.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
