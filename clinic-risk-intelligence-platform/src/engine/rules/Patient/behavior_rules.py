from src.engine.rules.base import RiskRule

from collections import Counter

class RepeatedPatientAccessRule(RiskRule):
    RULE_TYPE = "batch"

    def evaluate(self, event, context=None):
        return None

    def evaluate_batch(self, events, context=None):
        findings = []

        if not context:
            return findings

        user_activity = context.get("user_activity", {})

        for user, resources in user_activity.items():
            counts = Counter(resources)

            for patient_id, count in counts.items():
                if count > 5:
                    findings.append({
                        "rule_name": "Repeated Patient Access",
                        "category": "BEHAVIORAL",
                        "severity": "MEDIUM",
                        "user": user,
                        "patient_id": patient_id,
                        "count": count
                    })

        return findings
    


