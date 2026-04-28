from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.storage.database import get_db
from src.services.reporting_service import ReportingService

router = APIRouter()
service = ReportingService()


@router.get("/summary")
def clinic_summary(db: Session = Depends(get_db)):
    return service.get_clinic_risk_summary(db)


@router.get("/trend")
def risk_trend(db: Session = Depends(get_db)):
    return service.get_risk_trend(db)


@router.get("/top-users")
def top_users(db: Session = Depends(get_db)):
    return service.get_top_risk_users(db)


@router.get("/top-rules")
def top_rules(db: Session = Depends(get_db)):
    return service.get_top_risk_rules(db)