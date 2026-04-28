from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.storage.models_sql import EventRecord

from src.storage.database import get_db
from src.engine.rule_engine import RuleEngine
from src.services.event_service import EventService

router = APIRouter()

engine = RuleEngine()
service = EventService(engine)


@router.post("/ingest")
def ingest_event(system: str, payload: dict, db: Session = Depends(get_db)):

    event, findings = service.process_event(system, payload, db=db)

    return {
        "event_id": event.event_id,
        "risk_score": event.risk_score,
        "risk_flags": event.risk_flags,
        "findings": findings
    }


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    """
    Returns high-risk events for operational monitoring.
    """

    alerts = (
        db.query(EventRecord)
        .filter(EventRecord.risk_score >= 60)
        .order_by(EventRecord.timestamp.desc())
        .limit(50)
        .all()
    )

    return [
        {
            "event_id": a.id,
            "user_id": a.user_id,
            "risk_score": a.risk_score,
            "flags": a.risk_flags,
            "timestamp": a.timestamp
        }
        for a in alerts
    ]