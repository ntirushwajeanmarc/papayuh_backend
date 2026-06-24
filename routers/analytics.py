from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Citizen, CitizenRequest, Report, TrainingRegistration, WiFiSession

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return {
        "total_citizens": db.query(Citizen).count(),
        "total_requests": db.query(CitizenRequest).count(),
        "total_reports": db.query(Report).count(),
        "youth_trained": db.query(TrainingRegistration).filter(TrainingRegistration.certified == True).count(),
        "active_wifi_sessions": db.query(WiFiSession).filter(WiFiSession.is_active == True).count(),
    }
