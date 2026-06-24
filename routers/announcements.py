from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import Announcement

router = APIRouter(prefix="/announcements", tags=["Announcements"])

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    target_audience: Optional[str] = None
    target_id: Optional[str] = None
    push_notification: bool = False

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    push_notification: Optional[bool] = None

@router.get("/")
def list_announcements(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    return db.query(Announcement).order_by(Announcement.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/", status_code=201)
def create_announcement(data: AnnouncementCreate, db: Session = Depends(get_db)):
    announcement = Announcement(**data.model_dump(), author_id=1)  # TODO: get from auth
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return announcement

@router.put("/{id}")
def update_announcement(id: int, data: AnnouncementUpdate, db: Session = Depends(get_db)):
    ann = db.query(Announcement).filter(Announcement.id == id).first()
    if not ann:
        raise HTTPException(404, "Announcement not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(ann, key, val)
    db.commit()
    return ann

@router.delete("/{id}")
def delete_announcement(id: int, db: Session = Depends(get_db)):
    ann = db.query(Announcement).filter(Announcement.id == id).first()
    if not ann:
        raise HTTPException(404)
    db.delete(ann)
    db.commit()
    return {"message": "Deleted"}
