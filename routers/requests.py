from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import CitizenRequest

router = APIRouter(prefix="/requests", tags=["Citizen Requests"])

class RequestCreate(BaseModel):
    request_type: str
    title: str
    description: Optional[str] = None

class RequestUpdate(BaseModel):
    status: Optional[str] = None
    feedback: Optional[str] = None

@router.get("/")
def list_requests(db: Session = Depends(get_db), skip: int = 0, limit: int = 50, status: Optional[str] = None):
    q = db.query(CitizenRequest)
    if status:
        q = q.filter(CitizenRequest.status == status)
    return q.offset(skip).limit(limit).all()

@router.post("/", status_code=201)
def create_request(data: RequestCreate, db: Session = Depends(get_db)):
    req = CitizenRequest(**data.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

@router.put("/{id}")
def update_request(id: int, data: RequestUpdate, db: Session = Depends(get_db)):
    req = db.query(CitizenRequest).filter(CitizenRequest.id == id).first()
    if not req:
        raise HTTPException(404)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(req, k, v)
    db.commit()
    return req
