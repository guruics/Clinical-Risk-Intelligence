from typing import List, Type
from collections import defaultdict
import inspect

from src.engine.rules.base import RiskRule
from src.engine.rules.Patient import (
    access_rules,
    anamoly_rules,
    behavior_rules,
    clinical_context_rules
)



class RuleRegistry:
    """
    Central registry for all risk rules.

    Responsibilities:
    - Discover rule classes
    - Maintain API → rule mapping
    - Separate event vs batch rules
    - Instantiate rules safely
    """

    _instance = None

    # -------------------------------------------------
    # Singleton
    # -------------------------------------------------
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RuleRegistry, cls).__new__(cls)

            cls._instance._rule_classes = []
            cls._instance._api_index = defaultdict(list)

            cls._instance._initialize()

        return cls._instance

    # -------------------------------------------------
    # One-time initialization
    # -------------------------------------------------
    def _initialize(self):
        """
        Initialize registry ONCE.
        """
        self.auto_discover([
            access_rules,
            anamoly_rules,
            behavior_rules,
            clinical_context_rules
        ])

        self._build_api_index()

    # -------------------------------------------------
    # Registration
    # -------------------------------------------------
    def register(self, rule_class: Type[RiskRule]):
        """
        Register rule class safely (no duplicates)
        """
        if rule_class in self._rule_classes:
            return

        self._rule_classes.append(rule_class)

    # -------------------------------------------------
    # Auto-discovery
    # -------------------------------------------------
    def auto_discover(self, module_list: List):
        for module in module_list:
            for attr_name in dir(module):
                attr = getattr(module, attr_name)

                if (
                    isinstance(attr, type)
                    and issubclass(attr, RiskRule)
                    and attr is not RiskRule
                    and not inspect.isabstract(attr)
                ):
                    self.register(attr)

    # -------------------------------------------------
    # API Index Builder
    # -------------------------------------------------
    def _build_api_index(self):
        """
        Build API → rule mapping
        """
        for rule_class in self._rule_classes:
            apis = getattr(rule_class, "APPLIES_TO_APIS", ["*"])

            for api in apis:
                self._api_index[api].append(rule_class)

    # -------------------------------------------------
    # Rule Instantiation
    # -------------------------------------------------
    def _instantiate(self, rule_classes: List[Type[RiskRule]]) -> List[RiskRule]:
        instances = []

        for cls in rule_classes:
            try:
                instances.append(cls())
            except TypeError as e:
                print(f"[Registry Skip] {cls.__name__}: {e}")

        return instances

    # -------------------------------------------------
    # API-based resolution
    # -------------------------------------------------
    def get_rules_for_api(self, api_name: str) -> List[RiskRule]:
        print(f"[Registry] API requested: {api_name}")

        rule_classes = (
            self._api_index.get(api_name, []) +
            self._api_index.get("*", [])
        )

        # Deduplicate classes
        rule_classes = list(set(rule_classes))

        print(f"[Registry] Matched rules: {[cls.__name__ for cls in rule_classes]}")

        return self._instantiate(rule_classes)

    # -------------------------------------------------
    # Event rules
    # -------------------------------------------------
    def get_event_rules(self, api_name: str) -> List[RiskRule]:
        rules = self.get_rules_for_api(api_name)

        event_rules = []
        for r in rules:
            rule_type = getattr(r, "RULE_TYPE", "event").lower()

            if rule_type == "event":
                event_rules.append(r)

            # 🔥 validation
            elif rule_type == "batch" and hasattr(r, "evaluate"):
                pass  # ok, batch rule should not run here

        return event_rules

    # -------------------------------------------------
    # Batch rules
    # -------------------------------------------------
    def get_batch_rules(self) -> List[RiskRule]:
        batch_rules = []

        for cls in self._rule_classes:
            rule_type = getattr(cls, "RULE_TYPE", "event").lower()

            if rule_type == "batch":
                if not hasattr(cls, "evaluate_batch"):
                    print(f"[WARNING] {cls.__name__} marked batch but missing evaluate_batch()")
                    continue

                batch_rules.append(cls())

        return batch_rules

    # -------------------------------------------------
    # Utility
    # -------------------------------------------------
    def clear(self):
        self._rule_classes = []
        self._api_index = defaultdict(list)
        self._instance = None