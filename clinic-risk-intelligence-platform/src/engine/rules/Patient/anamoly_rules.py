from src.engine.rules.base import RiskRule

class ExcessivePatientSearchRule:
    RULE_TYPE="Batch"
    def evaluate(self, event, context=None):
        return None  # disable per-event

    def evaluate_batch(self, event, context=None):
        findings = []

        user_counts = context.get("user_patient_counts", {})

        for user, count in user_counts.items():
            if count > 10:  # threshold
                findings.append({
                    "rule_name": "Excessive Patient Search",
                    "category": "BEHAVIORAL",
                    "severity": "HIGH",
                    "user": user,
                    "count": count
                })

        return findings
    
class BulkPatientEnumerationRule(RiskRule):
    RULE_TYPE="Batch"
    APPLIES_TO_APIS = ["patients.search"]

    def evaluate(self, event, context=None):
        if event.event_type not in ["ACCESS", "PATIENT_SEARCH", "PATIENT_VIEW"]:
            return None

        if event.metadata.get("result_count", 0) > 10:
            return {
                "rule_name": "Bulk Patient Enumeration",
                "category": "SECURITY",
                "severity": "HIGH",
                "event_id": event.event_id
            }

        return None

from src.engine.rules.base import RiskRule


class CrossPatientRapidAccessRule(RiskRule):

    RULE_TYPE = "batch"
    APPLIES_TO_APIS = ["patients.search"]

    def evaluate(self, event, context=None):
        return None  # event-level disabled

    def evaluate_batch(self, events, context=None):
        """
        Detects rapid patient access behavior within time window.
        """

        findings = []

        if not events:
            return findings

        # Sort once
        events = sorted(events, key=lambda e: e.timestamp)

        window_seconds = 60
        threshold = 10

        # Group by user first (CRITICAL FIX)
        user_events = {}

        for e in events:
            user_events.setdefault(e.user_id, []).append(e)

        for user, evts in user_events.items():

            for i in range(len(evts)):
                base = evts[i]
                count = 1

                for j in range(i + 1, len(evts)):
                    delta = (evts[j].timestamp - base.timestamp).total_seconds()

                    if delta > window_seconds:
                        break

                    count += 1

                if count >= threshold:
                    findings.append({
                        "rule_name": "Rapid Cross-Patient Access",
                        "category": "BEHAVIORAL",
                        "severity": "HIGH",
                        "user": user,
                        "count": count,
                        "window_seconds": window_seconds
                    })
                    break

        return findings