# Access rules
from src.engine.rules.base import RiskRule

class UnauthorizedPHIAccessRule:
    def evaluate(self, event):
        if event.event_type == "ACCESS" and event.resource_type == "PATIENT":
            return {
                "rule_name": "Unauthorized PHI Access",
                "category": "PHI_ACCESS",
                "severity": "HIGH",
                "event_id": event.event_id
            }
        return None

class UnauthorizedPHIAccessRule1(RiskRule):

    def evaluate(self, event):
        if event.event_type != "ACCESS":
            return None

        if event.role in ["billing", "frontdesk", "reception"] and event.resource_type == "PATIENT":
            return {
                "rule": "UNAUTHORIZED_PHI_ACCESS",
                "severity": "HIGH",
                "message": "Non-clinical role accessed patient data",
                "event_id": event.event_id
            }

        return None

class AfterHoursAccessRule(RiskRule):

    def evaluate(self, event):
        if event.event_type != "ACCESS":
            return None

        hour = event.timestamp.hour

        if hour < 6 or hour > 20:
            return {
                "rule": "AFTER_HOURS_ACCESS",
                "severity": "MEDIUM",
                "message": "Access outside normal clinic hours",
                "event_id": event.event_id
            }

        return None
    

