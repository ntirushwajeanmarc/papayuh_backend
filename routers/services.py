from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import ServiceRequest

router = APIRouter(prefix="/services", tags=["Smart Services"])

class ServiceCreate(BaseModel):
    service_type: str
    description: Optional[str] = None

@router.get("/")
def list_services(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    return db.query(ServiceRequest).offset(skip).limit(limit).all()

@router.post("/", status_code=201)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    srv = ServiceRequest(**data.model_dump())
    db.add(srv)
    db.commit()
    db.refresh(srv)
    return srv
