import random
import uuid
from datetime import datetime, timedelta

from src.models.event import UnifiedEvent
from src.engine.rule_engine import RuleEngine

from src.engine.rules.access_rules import UnauthorizedPHIAccessRule, AfterHoursAccessRule
from src.engine.rules.billing_rules import BillingWithoutEncounterRule
from src.engine.rules.clinical_pattern_rules import (
    PrescriptionSpikeRule,
    LoginAnomalyRule,
    APIAccessRule
)


# -----------------------------
# CONFIG
# -----------------------------
USERS = [
    ("dr_smith", "clinician"),
    ("dr_jones", "clinician"),
    ("billing_1", "billing"),
    ("frontdesk_1", "frontdesk"),
    ("nurse_amy", "nurse")
]

EVENT_TYPES = ["ACCESS", "BILL", "PRESCRIBE", "LOGIN", "API_CALL"]

RESOURCE_TYPES = ["PATIENT", "CLAIM", "PRESCRIPTION", "USER"]

SYSTEMS = ["openemr", "athena", "ecw", "kareo"]


# -----------------------------
# ENGINE SETUP
# -----------------------------
def build_engine():
    engine = RuleEngine()

    engine.register_rule(UnauthorizedPHIAccessRule())
    engine.register_rule(AfterHoursAccessRule())
    engine.register_rule(BillingWithoutEncounterRule())
    engine.register_rule(PrescriptionSpikeRule())
    engine.register_rule(LoginAnomalyRule())
    engine.register_rule(APIAccessRule())

    return engine


# -----------------------------
# EVENT GENERATOR
# -----------------------------
def generate_event(i: int):
    user_id, role = random.choice(USERS)

    event_type = random.choice(EVENT_TYPES)
    system = random.choice(SYSTEMS)
    resource_type = random.choice(RESOURCE_TYPES)

    # introduce controlled risk patterns
    metadata = {}

    # BULK ACCESS SCENARIO
    if i % 15 == 0:
        metadata["records_accessed"] = random.randint(60, 200)

    # AFTER HOURS SCENARIO
    if i % 20 == 0:
        timestamp = datetime.utcnow().replace(hour=random.randint(0, 5))
    else:
        timestamp = datetime.utcnow()

    # LOGIN ANOMALY
    if i % 25 == 0:
        metadata["new_device"] = True

    # PRESCRIPTION SPIKE
    if i % 18 == 0:
        metadata["daily_prescriptions"] = random.randint(30, 80)

    return UnifiedEvent(
        event_id=str(uuid.uuid4()),
        timestamp=timestamp,
        system=system,
        user_id=user_id,
        role=role,
        event_type=event_type,
        resource_type=resource_type,
        resource_id=f"R-{random.randint(1000,9999)}",
        metadata=metadata
    )


# -----------------------------
# MAIN EXECUTION
# -----------------------------
def run_dataset(n=100):
    engine = build_engine()

    results = []

    for i in range(n):
        event = generate_event(i)
        findings = engine.evaluate(event)

        results.append({
            "event_id": event.event_id,
            "user_id": event.user_id,
            "event_type": event.event_type,
            "risk_flags": [f["rule"] for f in findings],
            "severity_count": len(findings)
        })

    return results


if __name__ == "__main__":
    dataset = run_dataset(100)

    print("\nGenerated Events: 100")
    print("Sample Output:\n")

    for d in dataset[:10]:
        print(d)