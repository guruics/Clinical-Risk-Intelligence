from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.storage.database import get_db
from src.storage.models_sql import EventRecord
from sqlalchemy import func

router = APIRouter()

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):

    events = db.query(EventRecord).all()

    if not events:
        return {
            "clinic_risk_index": 0,
            "event_count": 0,
            "high_risk_events": 0
        }

    total_risk = sum(e.risk_score or 0 for e in events)
    high_risk = len([e for e in events if (e.risk_score or 0) >= 60])

    return {
        "clinic_risk_index": round(total_risk / len(events), 2),
        "event_count": len(events),
        "high_risk_events": high_risk
    }

@router.get("/top-users")
def top_users(db: Session = Depends(get_db)):

    results = (
        db.query(
            EventRecord.user_id,
            func.avg(EventRecord.risk_score).label("avg_risk"),
            func.count(EventRecord.id).label("event_count")
        )
        .group_by(EventRecord.user_id)
        .order_by(func.avg(EventRecord.risk_score).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "user_id": r[0],
            "avg_risk_score": float(r[1] or 0),
            "event_count": r[2]
        }
        for r in results
    ]

@router.get("/role-risk")
def role_risk(db: Session = Depends(get_db)):

    results = (
        db.query(
            EventRecord.role,
            func.avg(EventRecord.risk_score),
            func.count(EventRecord.id)
        )
        .group_by(EventRecord.role)
        .all()
    )

    return [
        {
            "role": r[0],
            "avg_risk": float(r[1] or 0),
            "event_count": r[2]
        }
        for r in results
    ]

@router.get("/alerts")
def alerts(db: Session = Depends(get_db)):

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
            "role": a.role,
            "risk_score": a.risk_score,
            "flags": a.risk_flags,
            "timestamp": a.timestamp
        }
        for a in alerts
    ]

@router.get("/trend")
def risk_trend(db: Session = Depends(get_db)):

    results = (
        db.query(
            func.date(EventRecord.timestamp),
            func.avg(EventRecord.risk_score)
        )
        .group_by(func.date(EventRecord.timestamp))
        .order_by(func.date(EventRecord.timestamp))
        .all()
    )

    trend = [
        {"date": str(r[0]), "avg_risk": float(r[1] or 0)}
        for r in results
    ]

    # simple smoothing (moving average)
    for i in range(1, len(trend)):
        trend[i]["smoothed"] = round(
            (trend[i]["avg_risk"] + trend[i-1]["avg_risk"]) / 2,
            2
        )

    return trend