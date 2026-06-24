from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Message

router = APIRouter(prefix="/messages", tags=["Communication"])

class MessageCreate(BaseModel):
    receiver_id: Optional[int] = None
    group_type: Optional[str] = None
    group_id: Optional[str] = None
    subject: Optional[str] = None
    content: str

@router.get("/")
def list_messages(db: Session = Depends(get_db), user_id: int = 1, skip: int = 0, limit: int = 50):
    return db.query(Message).filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).offset(skip).limit(limit).all()

@router.post("/", status_code=201)
def send_message(data: MessageCreate, db: Session = Depends(get_db)):
    msg = Message(**data.model_dump(), sender_id=1)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
