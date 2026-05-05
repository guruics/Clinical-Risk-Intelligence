from src.engine.rules.base import RiskRule

class MissingEncounterContextRule(RiskRule):
    RULE_TYPE = "batch"
    APPLIES_TO_APIS = ["patients.search", "encounters.list"]

    def evaluate(self, event, context=None):
        return None  # event-level disabled

    def evaluate_batch(self, events, context=None):
        """
        Detects users accessing patients without encounter context.
        """

        findings = []

        if not events:
            return findings

        # Group by user
        user_events = {}

        for e in events:
            user_events.setdefault(e.user_id, []).append(e)

        for user, evts in user_events.items():
            total = len(evts)

            # check encounter presence
            has_encounter = any(
                getattr(e, "metadata", {}).get("encounter_id")
                for e in evts
            )

            if not has_encounter and total > 10:
                findings.append({
                    "rule_name": "Missing Encounter Context",
                    "category": "CLINICAL_CONTEXT",
                    "severity": "HIGH",
                    "user": user,
                    "count": total
                })

        return findings
    
class DeepPatientChartAccessRule(RiskRule):
    RULE_TYPE = "event"
    APPLIES_TO_APIS = ["patients.chart", "encounters.get"]

    def evaluate(self, event):
        if event.event_type not in ["ACCESS", "PATIENT_SEARCH", "PATIENT_VIEW"]:
            return None

        depth = event.metadata.get("chart_depth", 0)

        if depth > 5:
            return {
                "rule_name": "Deep Patient Chart Access",
                "category": "PHI_ACCESS",
                "severity": "CRITICAL",
                "event_id": event.event_id
            }

        return None