from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Citizen, Household

router = APIRouter(prefix="/citizens", tags=["Citizens"])

class CitizenCreate(BaseModel):
    national_id: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    village: Optional[str] = None
    cell: Optional[str] = None
    sector: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None

class HouseholdCreate(BaseModel):
    head_id: int
    ubudehe_category: Optional[str] = None
    house_type: Optional[str] = None
    members_count: int = 1
    address: Optional[str] = None
    village: Optional[str] = None
    cell: Optional[str] = None
    sector: Optional[str] = None

@router.get("/")
def list_citizens(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, village: Optional[str] = None):
    query = db.query(Citizen)
    if village:
        query = query.filter(Citizen.village == village)
    return query.offset(skip).limit(limit).all()

@router.post("/", status_code=201)
def create_citizen(data: CitizenCreate, db: Session = Depends(get_db)):
    existing = db.query(Citizen).filter(Citizen.national_id == data.national_id).first()
    if existing:
        raise HTTPException(400, "Citizen with this national ID already exists")
    citizen = Citizen(**data.model_dump())
    db.add(citizen)
    db.commit()
    db.refresh(citizen)
    return citizen

@router.get("/households/")
def list_households(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Household).offset(skip).limit(limit).all()

@router.post("/households/", status_code=201)
def create_household(data: HouseholdCreate, db: Session = Depends(get_db)):
    household = Household(**data.model_dump())
    db.add(household)
    db.commit()
    db.refresh(household)
    return household

@router.get("/{citizen_id}")
def get_citizen(citizen_id: int, db: Session = Depends(get_db)):
    citizen = db.query(Citizen).filter(Citizen.id == citizen_id).first()
    if not citizen:
        raise HTTPException(404, "Citizen not found")
    return citizen
