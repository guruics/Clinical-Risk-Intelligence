# Rule engine core
from typing import List
from src.models.event import UnifiedEvent


class RuleEngine:
    """
    Evaluates UnifiedEvents against registered risk rules.
    Produces RiskFindings that downstream scoring consumes.
    """

    def __init__(self):
        self.rules = []

    def register_rule(self, rule):
        self.rules.append(rule)

    def evaluate(self, event: UnifiedEvent) -> List[dict]:
        findings = []

        for rule in self.rules:
            result = rule.evaluate(event)
            if result:
                findings.append(result)

        return findings