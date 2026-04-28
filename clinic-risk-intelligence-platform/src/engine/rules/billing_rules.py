# Billing rules
from src.engine.rules.base import RiskRule

class BillingWithoutEncounterRule(RiskRule):

    def evaluate(self, event):
        if event.event_type != "BILL":
            return None

        if not event.resource_id:
            return {
                "rule": "BILLING_WITHOUT_ENCOUNTER",
                "severity": "HIGH",
                "message": "Billing event missing encounter linkage",
                "event_id": event.event_id
            }

        return None
    
class BulkDataAccessRule(RiskRule):

    def evaluate(self, event):
        if event.event_type != "ACCESS":
            return None

        if event.metadata.get("records_accessed", 0) > 50:
            return {
                "rule": "BULK_PHI_ACCESS",
                "severity": "CRITICAL",
                "message": "Large volume of patient records accessed",
                "event_id": event.event_id
            }

        return None

class DataExportRule(RiskRule):

    def evaluate(self, event):
        if event.event_type != "EXPORT":
            return None

        if event.metadata.get("export_size", 0) > 1000:
            return {
                "rule": "LARGE_DATA_EXPORT",
                "severity": "HIGH",
                "message": "Large dataset exported from system",
                "event_id": event.event_id
            }

        return None