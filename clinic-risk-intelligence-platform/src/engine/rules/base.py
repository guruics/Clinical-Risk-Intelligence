from abc import ABC, abstractmethod
from src.models.event import UnifiedEvent


class RiskRule(ABC):
    """
    Base class for all risk detection rules.
    """

    @abstractmethod
    def evaluate(self, event: UnifiedEvent):
        """
        Return:
            dict (risk finding) OR None
        """
        pass