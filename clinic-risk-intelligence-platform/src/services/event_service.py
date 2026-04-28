from src.normalization.event_mapper import EventMapper
from src.normalization.identity_resolver import IdentityResolver
from src.engine.rule_engine import RuleEngine
from src.scoring.risk_calculator import RiskCalculator
from src.scoring.domain_weights import DOMAIN_WEIGHTS

from src.storage.repository import EventRepository


class EventService:

    def __init__(self, rule_engine: RuleEngine):
        self.mapper = EventMapper()
        self.identity = IdentityResolver()
        self.rules = rule_engine
        self.scorer = RiskCalculator(DOMAIN_WEIGHTS)

        # NEW: persistence layer
        self.repo = EventRepository()

    def process_event(self, system: str, payload: dict, db=None):

        # 1. Normalize
        event = self.mapper.map(system, payload)

        # 2. Identity resolution
        event.user_id = self.identity.resolve(system, event.user_id)

        # 3. Rule evaluation
        findings = self.rules.evaluate(event)

        # 4. Risk scoring
        score = self.scorer.calculate_event_score(findings)

        event.risk_score = score
        event.risk_flags = [f["rule"] for f in findings]

        # 5. Persist (NEW)
        if db:
            self.repo.save_event(db, event)

        return event, findings