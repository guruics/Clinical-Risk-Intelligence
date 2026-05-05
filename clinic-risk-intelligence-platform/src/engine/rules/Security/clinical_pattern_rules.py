# Clinical pattern rules
from src.engine.rules.base import RiskRule

class PrescriptionSpikeRule(RiskRule):

    def evaluate(self, event):
        if event.event_type != "PRESCRIBE":
            return None

        if event.metadata.get("daily_prescriptions", 0) > 30:
            return {
                "rule": "PRESCRIPTION_SPIKE",
                "severity": "MEDIUM",
                "message": "Unusual prescription volume detected",
                "event_id": event.event_id
            }

        return None
    
class IdentityConflictRule(RiskRule):

    def evaluate(self, event):
        if event.metadata.get("cross_system_behavior", False):
            return {
                "rule": "IDENTITY_CONFLICT",
                "severity": "HIGH",
                "message": "Same user behaving inconsistently across systems",
                "event_id": event.event_id
            }

        return None
    
class LoginAnomalyRule(RiskRule):

    def evaluate(self, event):
        if event.event_type != "LOGIN":
            return None

        if event.metadata.get("new_device", False):
            return {
                "rule": "NEW_DEVICE_LOGIN",
                "severity": "MEDIUM",
                "message": "Login from unrecognized device",
                "event_id": event.event_id
            }

        return None
    
class APIAccessRule(RiskRule):

    def evaluate(self, event):
        if event.event_type != "API_CALL":
            return None

        if event.metadata.get("unauthenticated", False):
            return {
                "rule": "UNAUTHENTICATED_API_ACCESS",
                "severity": "CRITICAL",
                "message": "Unsecured API endpoint accessed",
                "event_id": event.event_id
            }

        return None
    

