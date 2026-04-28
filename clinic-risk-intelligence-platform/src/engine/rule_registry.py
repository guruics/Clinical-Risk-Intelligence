from typing import List, Type
from src.engine.rules.base import RiskRule


class RuleRegistry:
    """
    Central registry for all risk rules.

    Responsibilities:
    - Register rule classes
    - Instantiate rule objects
    - Provide rule list to RuleEngine
    """

    def __init__(self):
        self._rule_classes: List[Type[RiskRule]] = []

    def register(self, rule_class: Type[RiskRule]):
        """
        Register a rule class (not instance).
        """
        if rule_class not in self._rule_classes:
            self._rule_classes.append(rule_class)

    def load_rules(self) -> List[RiskRule]:
        """
        Instantiate all registered rules.
        """
        return [rule_class() for rule_class in self._rule_classes]

    def auto_discover(self, module_list: List):
        """
        Optional helper for manual module-based loading.

        Example usage:
            registry.auto_discover([
                access_rules,
                billing_rules
            ])
        """
        for module in module_list:
            for attr_name in dir(module):
                attr = getattr(module, attr_name)

                if (
                    isinstance(attr, type)
                    and hasattr(attr, "evaluate")
                ):
                    self.register(attr)

    def clear(self):
        """
        Reset registry (useful for tests).
        """
        self._rule_classes = []