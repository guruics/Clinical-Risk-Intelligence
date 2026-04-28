# Reporting service
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.storage.models_sql import EventRecord


class ReportingService:

    def get_clinic_risk_summary(self, db: Session):
        """
        Aggregates clinic-wide risk metrics.
        """

        events = db.query(EventRecord).all()

        if not events:
            return {
                "clinic_risk_index": 0,
                "event_count": 0
            }

        avg_risk = sum(e.risk_score or 0 for e in events) / len(events)

        return {
            "clinic_risk_index": round(avg_risk, 2),
            "event_count": len(events)
        }

    def get_risk_trend(self, db: Session):
        """
        Simple time-based risk trend (MVP version).
        """

        results = (
            db.query(
                func.date(EventRecord.timestamp),
                func.avg(EventRecord.risk_score)
            )
            .group_by(func.date(EventRecord.timestamp))
            .order_by(func.date(EventRecord.timestamp))
            .all()
        )

        return [
            {"date": str(r[0]), "risk_score": float(r[1] or 0)}
            for r in results
        ]

    def get_top_risk_users(self, db: Session, limit: int = 10):
        """
        Users contributing most to risk exposure.
        """

        results = (
            db.query(
                EventRecord.user_id,
                func.avg(EventRecord.risk_score).label("avg_risk")
            )
            .group_by(EventRecord.user_id)
            .order_by(func.avg(EventRecord.risk_score).desc())
            .limit(limit)
            .all()
        )

        return [
            {"user_id": r[0], "risk_score": float(r[1] or 0)}
            for r in results
        ]

    def get_top_risk_rules(self, db: Session, limit: int = 10):
        """
        Most frequently triggered risk patterns.
        """

        results = (
            db.query(EventRecord.risk_flags)
            .all()
        )

        counter = {}

        for r in results:
            flags = r[0] or []
            for f in flags:
                counter[f] = counter.get(f, 0) + 1

        sorted_rules = sorted(counter.items(), key=lambda x: x[1], reverse=True)

        return [
            {"rule": k, "count": v}
            for k, v in sorted_rules[:limit]
        ]