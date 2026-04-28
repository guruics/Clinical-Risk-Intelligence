from sqlalchemy.orm import Session

from src.storage.database import SessionLocal
from src.storage.repository import EventRepository

from src.engine.rule_engine import RuleEngine
from src.engine.rules.access_rules import UnauthorizedPHIAccessRule, AfterHoursAccessRule
from src.engine.rules.billing_rules import BillingWithoutEncounterRule
from src.engine.rules.clinical_pattern_rules import (
    PrescriptionSpikeRule,
    LoginAnomalyRule,
    APIAccessRule
)

from seed_synthetic_events import generate_event


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
# LOAD DATA
# -----------------------------
def load_to_db(n=200):
    db: Session = SessionLocal()
    repo = EventRepository()
    engine = build_engine()

    print(f"Loading {n} synthetic events into DB...")

    for i in range(n):
        event = generate_event(i)

        # Run rule engine (important for realism)
        findings = engine.evaluate(event)

        # attach risk outputs
        event.risk_flags = [f["rule"] for f in findings]
        event.risk_score = len(findings) * 25  # simple MVP scoring fallback

        # persist
        repo.save_event(db, event)

    db.close()

    print("Done. Synthetic dataset loaded into database.")


if __name__ == "__main__":
    load_to_db(200)