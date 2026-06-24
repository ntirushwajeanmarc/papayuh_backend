from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Report

router = APIRouter(prefix="/reports", tags=["Reports"])

class ReportCreate(BaseModel):
    title: str
    content: str
    report_type: str
    level: str

@router.get("/")
def list_reports(db: Session = Depends(get_db), skip: int = 0, limit: int = 50, report_type: Optional[str] = None):
    q = db.query(Report)
    if report_type:
        q = q.filter(Report.report_type == report_type)
    return q.order_by(Report.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/", status_code=201)
def create_report(data: ReportCreate, db: Session = Depends(get_db)):
    report = Report(**data.model_dump(), submitted_by=1)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
