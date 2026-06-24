from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import SMSNotification

router = APIRouter(prefix="/sms", tags=["SMS Notifications"])

class SMSCreate(BaseModel):
    recipient_phone: str
    message: str
    notification_type: Optional[str] = None

@router.get("/")
def list_sms(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    return db.query(SMSNotification).offset(skip).limit(limit).all()

@router.post("/", status_code=201)
def send_sms(data: SMSCreate, db: Session = Depends(get_db)):
    sms = SMSNotification(**data.model_dump())
    db.add(sms)
    db.commit()
    db.refresh(sms)
    return sms
