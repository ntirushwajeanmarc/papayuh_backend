from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import WiFiSession, WiFiHotspot

router = APIRouter(prefix="/wifi", tags=["WiFi Management"])

class HotspotCreate(BaseModel):
    name: str
    location: Optional[str] = None
    village: Optional[str] = None
    cell: Optional[str] = None
    sector: Optional[str] = None

@router.get("/hotspots/")
def list_hotspots(db: Session = Depends(get_db)):
    return db.query(WiFiHotspot).all()

@router.post("/hotspots/", status_code=201)
def create_hotspot(data: HotspotCreate, db: Session = Depends(get_db)):
    hs = WiFiHotspot(**data.model_dump())
    db.add(hs)
    db.commit()
    db.refresh(hs)
    return hs

@router.get("/sessions/")
def list_sessions(db: Session = Depends(get_db), active_only: bool = False):
    q = db.query(WiFiSession)
    if active_only:
        q = q.filter(WiFiSession.is_active == True)
    return q.all()
