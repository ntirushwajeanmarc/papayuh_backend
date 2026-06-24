from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import DigitalDocument

router = APIRouter(prefix="/documents", tags=["Digital Documents"])

class DocumentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    file_url: str
    file_type: Optional[str] = None
    file_size_kb: Optional[float] = None

@router.get("/")
def list_documents(db: Session = Depends(get_db), category: Optional[str] = None):
    q = db.query(DigitalDocument).filter(DigitalDocument.is_archived == False)
    if category:
        q = q.filter(DigitalDocument.category == category)
    return q.all()

@router.post("/", status_code=201)
def create_document(data: DocumentCreate, db: Session = Depends(get_db)):
    doc = DigitalDocument(**data.model_dump())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc
