from datetime import datetime

from src.models.event import UnifiedEvent
from src.engine.rule_engine import RuleEngine

# Import rules
from src.engine.rules.access_rules import UnauthorizedPHIAccessRule, AfterHoursAccessRule
from src.engine.rules.billing_rules import BillingWithoutEncounterRule
from src.engine.rules.clinical_pattern_rules import (
    PrescriptionSpikeRule,
    LoginAnomalyRule,
    APIAccessRule
)


def build_engine():
    engine = RuleEngine()

    # Register rules manually (MVP)
    engine.register_rule(UnauthorizedPHIAccessRule())
    engine.register_rule(AfterHoursAccessRule())
    engine.register_rule(BillingWithoutEncounterRule())
    engine.register_rule(PrescriptionSpikeRule())
    engine.register_rule(LoginAnomalyRule())
    engine.register_rule(APIAccessRule())

    return engine


def test_unauthorized_access():
    engine = build_engine()

    event = UnifiedEvent(
        event_id="test-1",
        timestamp=datetime.utcnow(),
        system="openemr",
        user_id="staff_1",
        role="billing",
        event_type="ACCESS",
        resource_type="PATIENT"
    )

    findings = engine.evaluate(event)

    print("\nTest: Unauthorized Access")
    print(findings)


def test_bulk_access():
    engine = build_engine()

    event = UnifiedEvent(
        event_id="test-2",
        timestamp=datetime.utcnow(),
        system="openemr",
        user_id="staff_2",
        role="reception",
        event_type="ACCESS",
        resource_type="PATIENT",
        metadata={"records_accessed": 120}
    )

    findings = engine.evaluate(event)

    print("\nTest: Bulk Access")
    print(findings)


def test_billing_issue():
    engine = build_engine()

    event = UnifiedEvent(
        event_id="test-3",
        timestamp=datetime.utcnow(),
        system="openemr",
        user_id="billing_1",
        role="billing",
        event_type="BILL",
        resource_type="CLAIM"
    )

    findings = engine.evaluate(event)

    print("\nTest: Billing Without Encounter")
    print(findings)


if __name__ == "__main__":
    test_unauthorized_access()
    test_bulk_access()
    test_billing_issue()