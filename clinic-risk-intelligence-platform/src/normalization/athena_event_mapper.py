import time
from datetime import datetime
from typing import Dict, List, Any

from src.models.event import UnifiedEvent, EventType, ResourceType, SystemType


class AthenaEventMapper:
    """
    Converts Athena API responses into UnifiedEvent objects
    for ingestion into the Risk Intelligence Engine.
    """
    print("I am in AthenaEventMapper _ 0")
    def __init__(self):
        self.system = SystemType.ATHENA if hasattr(SystemType, "ATHENA") else "ATHENA"

    def map_patient_search_response(
        self,
        response: Dict[str, Any],
        actor_user_id: str = "athena_system"
    ) -> List[UnifiedEvent]:
        """
        Converts Athena patient search results → UnifiedEvents
        """
        print("I am in AthenaEventMapper.map_patient_search_response _ 0")
        patients = response.get("patients", [])
        events: List[UnifiedEvent] = []

        for patient in patients:
            print("I am in AthenaEventMapper.map_patient_search_response _ 1")
            event = self._map_single_patient(patient, actor_user_id)
            events.append(event)

        return events

    def _map_single_patient(
        self,
        patient: Dict[str, Any],
        actor_user_id: str
    ) -> UnifiedEvent:

        patient_id = patient.get("patientid")

        # Athena does NOT always provide timestamp → use ingestion time
        now = datetime.now()

        return UnifiedEvent(
            event_id=f"athena-patient-{patient_id}-{now.timestamp()}",
            system="athena",
            event_type="ACCESS",  # patient lookup = PHI access event
            resource_type="PATIENT",
            resource_id=str(patient_id),

            user_id=actor_user_id,

            role="SYSTEM_API",

            timestamp=now,

            metadata={
                "source": "athena",
                "firstname": patient.get("firstname"),
                "lastname": patient.get("lastname"),
                "dob": patient.get("dob"),
                "sex": patient.get("sex"),
                "state": patient.get("state"),
                "zip": patient.get("zip"),
                "raw": patient,
                "athena_api": "patients.search",   # 🔥 REQUIRED
                "endpoint": "/v1/{practiceid}/patients/search",
                "module": "PATIENT"
            }
        )