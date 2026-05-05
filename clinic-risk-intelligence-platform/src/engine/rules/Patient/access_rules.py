# Access rules
from datetime import timezone
from multiprocessing import context

from src.engine.rules.base import RiskRule


# 🔴 Rule 1: Unauthorized PHI Access (role-based)
class UnauthorizedPHIAccessRule(RiskRule):
    RULE_TYPE = "event"
    APPLIES_TO_APIS = [
        "patients.search",
        "patients.get"
    ]

    def evaluate(self, event, context=None):
        if event.event_type not in ["ACCESS", "PATIENT_SEARCH", "PATIENT_VIEW"]:
            return None

        if event.resource_type == "PATIENT" and event.role in ["billing", "frontdesk", "reception"]:
            return {
                "rule_name": "Unauthorized PHI Access",
                "category": "PHI_ACCESS",
                "severity": "HIGH",
                "event_id": event.event_id
            }
        return None

class SystemBulkAccessRule(RiskRule):
    RULE_TYPE = "event"
    APPLIES_TO_APIS = ["patients.search"]

    def evaluate(self, event, context=None):
        if not context:
            return None

        user = getattr(event, "user_id", None)
        if not user:
            return None

        user_counts = context.get("user_patient_counts", {})
        count = user_counts.get(user, 0)

        if count <= 5:
            return None

        # 🔥 CRITICAL FIX: emit only once per user
        already_flagged = context.setdefault("_bulk_flagged_users", set())

        if user in already_flagged:
            return None

        already_flagged.add(user)

        return {
            "rule_name": "System-Level Bulk Patient Access",
            "category": "SYSTEM_ACCESS",
            "severity": "MEDIUM",
            "event_id": "batch",   # 🔥 not tied to single event
            "user": user,
            "count": count
        }

    def evaluate_batch(self, events, context=None):
        # intentionally unused
        return []

class RepeatedLastNameAccessRule(RiskRule):
    RULE_TYPE = "batch"
    APPLIES_TO_APIS = ["patients.search"]

    def evaluate(self, event, context=None):
        return None

    def evaluate_batch(self, events, context=None):
        lastnames = [
            e.metadata.get("lastname")
            for e in events
            if hasattr(e, "metadata")
        ]

        if lastnames.count("JOHN") > 10:
            return [{
                "rule_name": "High Volume Same Last Name Access",
                "category": "ANOMALY",
                "severity": "MEDIUM",
                "event_id": "batch"
            }]

        return []


# 🟠 Rule 2: After Hours Access
class AfterHoursAccessRule(RiskRule):
    RULE_TYPE = "event"
    def evaluate(self, event, context=None):
        if event.event_type not in ["ACCESS", "PATIENT_SEARCH", "PATIENT_VIEW"]:
            return None

        from datetime import timezone
        print("Event timestamp:", event.timestamp)
        hour = event.timestamp.hour
        print("Hour is :", hour)
        if hour < 6 or hour > 20:
            return {
                "rule_name": "After Hours Access",
                "category": "COMPLIANCE",
                "severity": "MEDIUM",
                "event_id": event.event_id
            }

        return None
    
    def evaluate_batch(self, events, context=None):
        return []


# 🔴 Rule 3: No Encounter Context (NEW)
class NoEncounterAccessRule(RiskRule):
    RULE_TYPE="event"
    def evaluate(self, event, context=None):
        return None
    
class UnauthorizedRoleAccessRule(RiskRule):
    RULE_TYPE="event"
    APPLIES_TO_APIS = ["patients.search", "encounters.list"]

    def evaluate(self, event, context=None):
        if event.event_type not in ["ACCESS", "PATIENT_SEARCH", "PATIENT_VIEW"]:
            return None

        restricted_roles = ["billing", "frontdesk", "reception", "intern"]

        if event.role in restricted_roles:
            return {
                "rule_name": "Unauthorized Role Access",
                "category": "PHI_ACCESS",
                "severity": "HIGH",
                "event_id": event.event_id
            }

        return None