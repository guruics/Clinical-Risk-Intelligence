from datetime import datetime

from src.models.event import UnifiedEvent
from src.engine.rule_engine import RuleEngine

from src.engine.rules.access_rules import UnauthorizedPHIAccessRule, AfterHoursAccessRule
from src.engine.rules.billing_rules import BillingWithoutEncounterRule
from src.engine.rules.clinical_pattern_rules import (
    PrescriptionSpikeRule,
    LoginAnomalyRule,
    APIAccessRule
)


def build_engine():
    engine = RuleEngine()

    engine.register_rule(UnauthorizedPHIAccessRule())
    engine.register_rule(AfterHoursAccessRule())
    engine.register_rule(BillingWithoutEncounterRule())
    engine.register_rule(PrescriptionSpikeRule())
    engine.register_rule(LoginAnomalyRule())
    engine.register_rule(APIAccessRule())

    return engine


def run_tests():
    engine = build_engine()

    tests = [
        {
            "name": "Unauthorized PHI Access",
            "event": UnifiedEvent(
                event_id="t1",
                timestamp=datetime.utcnow(),
                system="openemr",
                user_id="billing_user",
                role="billing",
                event_type="ACCESS",
                resource_type="PATIENT"
            )
        },
        {
            "name": "Bulk Access Scenario",
            "event": UnifiedEvent(
                event_id="t2",
                timestamp=datetime.utcnow(),
                system="openemr",
                user_id="staff_1",
                role="reception",
                event_type="ACCESS",
                resource_type="PATIENT",
                metadata={"records_accessed": 120}
            )
        },
        {
            "name": "Billing Without Encounter",
            "event": UnifiedEvent(
                event_id="t3",
                timestamp=datetime.utcnow(),
                system="openemr",
                user_id="billing_2",
                role="billing",
                event_type="BILL",
                resource_type="CLAIM"
            )
        }
    ]

    for t in tests:
        findings = engine.evaluate(t["event"])

        print("\n==============================")
        print(f"Test: {t['name']}")
        print("Findings:", findings)


if __name__ == "__main__":
    run_tests()