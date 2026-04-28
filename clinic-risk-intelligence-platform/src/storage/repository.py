# Data access layer
from sqlalchemy.orm import Session
from src.storage.models_sql import EventRecord, RiskAggregate


class EventRepository:

    def save_event(self, db: Session, event):
        record = EventRecord(
            id=event.event_id,
            timestamp=event.timestamp,
            system=event.system,
            user_id=event.user_id,
            role=event.role,
            event_type=event.event_type,
            resource_type=event.resource_type,
            resource_id=event.resource_id,
            risk_score=event.risk_score,
            risk_flags=event.risk_flags,
            raw_payload=event.raw_payload
        )

        db.add(record)
        db.commit()
        return record


class RiskRepository:

    def save_aggregate(self, db: Session, user_id: str, score: float, count: int):
        agg = RiskAggregate(
            user_id=user_id,
            clinic_risk_index=score,
            event_count=count
        )

        db.add(agg)
        db.commit()
        return agg