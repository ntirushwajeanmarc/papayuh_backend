from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import CommunityProject, ProjectProgress

router = APIRouter(prefix="/projects", tags=["Community Projects"])

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    budget_total: Optional[float] = None
    status: str = "Planned"
    village: Optional[str] = None
    cell: Optional[str] = None
    sector: Optional[str] = None

@router.get("/")
def list_projects(db: Session = Depends(get_db), status: Optional[str] = None):
    q = db.query(CommunityProject)
    if status:
        q = q.filter(CommunityProject.status == status)
    return q.all()

@router.post("/", status_code=201)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    p = CommunityProject(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.post("/{project_id}/progress/", status_code=201)
def report_progress(project_id: int, progress: float, report: str = "", db: Session = Depends(get_db)):
    pp = ProjectProgress(project_id=project_id, progress_percentage=progress, report=report)
    db.add(pp)
    db.commit()
    db.refresh(pp)
    return pp
