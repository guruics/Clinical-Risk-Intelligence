# SQL models
from sqlalchemy import Column, String, Float, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class EventRecord(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    system = Column(String)
    user_id = Column(String)
    role = Column(String)

    event_type = Column(String)
    resource_type = Column(String)
    resource_id = Column(String)

    risk_score = Column(Float)
    risk_flags = Column(JSON)

    raw_payload = Column(JSON)


class RiskAggregate(Base):
    __tablename__ = "risk_aggregates"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(String)
    clinic_risk_index = Column(Float)

    event_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)