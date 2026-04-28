from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
from datetime import datetime


EventType = Literal[
    "ACCESS",
    "MODIFY",
    "BILL",
    "PRESCRIBE",
    "EXPORT",
    "LOGIN",
    "LOGOUT",
    "SYSTEM",
    "API_CALL"
]

SystemType = Literal[
    "openemr",
    "athena",
    "ecw",
    "kareo",
    "hl7",
    "fhir",
    "unknown"
]

ResourceType = Literal[
    "PATIENT",
    "ENCOUNTER",
    "CLAIM",
    "PRESCRIPTION",
    "USER",
    "SYSTEM",
    "BILLING_RECORD",
    "API_RESOURCE",
    "UNKNOWN"
]


class UnifiedEvent(BaseModel):
    """
    Canonical event object for all healthcare system activity.
    Every connector MUST output this schema.
    """

    # -------------------------
    # Identity & Source
    # -------------------------
    event_id: str = Field(..., description="Unique event identifier")
    timestamp: datetime

    system: SystemType
    source_connector: Optional[str] = None

    # -------------------------
    # Actor (who did it)
    # -------------------------
    user_id: str
    role: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None

    # -------------------------
    # Action (what happened)
    # -------------------------
    event_type: EventType
    action: Optional[str] = None

    # -------------------------
    # Target (what was affected)
    # -------------------------
    resource_type: ResourceType
    resource_id: Optional[str] = None

    # -------------------------
    # Context
    # -------------------------
    department: Optional[str] = None
    location: Optional[str] = None

    # -------------------------
    # Risk Enrichment (computed later)
    # -------------------------
    risk_flags: Optional[list[str]] = Field(default_factory=list)
    risk_score: Optional[float] = None
    risk_domain: Optional[str] = None

    # -------------------------
    # Raw payload (important for traceability)
    # -------------------------
    raw_payload: Optional[Dict[str, Any]] = None

    # -------------------------
    # Extensibility hook (future AI layer)
    # -------------------------
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        extra = "forbid"  # prevents schema drift (important in healthcare)