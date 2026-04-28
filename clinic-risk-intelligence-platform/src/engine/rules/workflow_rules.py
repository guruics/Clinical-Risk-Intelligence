# Workflow rules
from src.engine.rules.base import RiskRule
class RoleViolationRule(RiskRule):

    def evaluate(self, event):
        if event.role == "billing" and event.event_type == "MODIFY":
            if event.resource_type == "PATIENT":
                return {
                    "rule": "ROLE_VIOLATION",
                    "severity": "HIGH",
                    "message": "Billing role modifying clinical data",
                    "event_id": event.event_id
                }

        return None
    
