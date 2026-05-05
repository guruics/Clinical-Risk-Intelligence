from abc import ABC, abstractmethod
from src.models.event import UnifiedEvent


class RiskRule(ABC):
    """
    Base class for all risk detection rules.
    """
    RULE_TYPE = "event"  # or "batch"

    def evaluate(self, event, context=None):
        return None

    def evaluate_batch(self, events, context=None):
        return None