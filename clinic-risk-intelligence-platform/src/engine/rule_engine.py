# Rule engine core
from typing import List
from src.models.event import UnifiedEvent
from src.engine.rule_registry import RuleRegistry


class RuleEngine:
    """
    Evaluates UnifiedEvents against registered risk rules.
    Produces RiskFindings that downstream scoring consumes.
    """

    def __init__(self):
        self.registry = RuleRegistry()

    def evaluate(self, event: UnifiedEvent, context=None) -> List[dict]:
        findings = []
        print("Evaluating event in RuleEngine:", event)

        # ---------------------------------
        # Resolve API
        # ---------------------------------
        api = event.metadata.get("athena_api", "unknown")

        # ---------------------------------
        # Fetch rules (DO NOT store in self.rules)
        # ---------------------------------
        rules = self.registry.get_rules_for_api(api)

        # ---------------------------------
        # Execute rules safely
        # ---------------------------------
        for rule in rules:
            try:
                result = rule.evaluate(event, context)
                if not result:
                    continue

                if isinstance(result, list):
                    findings.extend(result)
                else:
                    findings.append(result)

            except Exception as e:
                print(f"[ERROR] {rule.__class__.__name__}: {e}")

        return findings