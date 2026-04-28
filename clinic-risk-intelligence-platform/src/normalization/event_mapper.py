# Event normalization
from datetime import datetime
from typing import Dict, Any
import uuid

from src.models.event import UnifiedEvent


class EventMapper:
    """
    Converts raw system-specific payloads into UnifiedEvent objects.
    This is the ONLY entry point from connectors into the system.
    """

    def map(self, system: str, payload: Dict[str, Any], connector_name: str = None) -> UnifiedEvent:
        """
        Main normalization function.
        """

        event_type = self._infer_event_type(payload)
        resource_type = self._infer_resource_type(payload)

        return UnifiedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=self._extract_timestamp(payload),

            system=system,
            source_connector=connector_name,

            user_id=self._extract_user_id(payload),
            role=payload.get("role"),

            event_type=event_type,
            action=payload.get("action"),

            resource_type=resource_type,
            resource_id=payload.get("resource_id"),

            department=payload.get("department"),
            location=payload.get("location"),

            raw_payload=payload,
            metadata=payload.get("metadata", {})
        )

    # -------------------------
    # Extraction helpers
    # -------------------------

    def _extract_user_id(self, payload: Dict[str, Any]) -> str:
        return (
            payload.get("user_id")
            or payload.get("user")
            or payload.get("actor_id")
            or "unknown"
        )

    def _extract_timestamp(self, payload: Dict[str, Any]) -> datetime:
        ts = payload.get("timestamp")
        if isinstance(ts, datetime):
            return ts
        if ts:
            return datetime.fromisoformat(ts)
        return datetime.utcnow()

    # -------------------------
    # Inference logic
    # -------------------------

    def _infer_event_type(self, payload: Dict[str, Any]) -> str:
        action = (payload.get("action") or "").lower()

        if "login" in action:
            return "LOGIN"
        if "bill" in action:
            return "BILL"
        if "prescribe" in action:
            return "PRESCRIBE"
        if "export" in action:
            return "EXPORT"
        if "modify" in action or "update" in action:
            return "MODIFY"
        if "access" in action or "view" in action:
            return "ACCESS"

        return payload.get("event_type", "SYSTEM")

    def _infer_resource_type(self, payload: Dict[str, Any]) -> str:
        rtype = (payload.get("resource_type") or "").lower()

        mapping = {
            "patient": "PATIENT",
            "encounter": "ENCOUNTER",
            "claim": "CLAIM",
            "prescription": "PRESCRIPTION",
            "billing": "BILLING_RECORD",
            "user": "USER"
        }

        return mapping.get(rtype, "UNKNOWN")