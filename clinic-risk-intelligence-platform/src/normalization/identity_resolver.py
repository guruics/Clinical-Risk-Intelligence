# Identity mapping
from typing import Dict, Optional


class IdentityResolver:
    """
    Resolves users across multiple healthcare systems
    into a single canonical identity.
    """

    def __init__(self):
        # MVP: in-memory mapping
        # later: move to database table
        self.identity_map: Dict[str, str] = {}

    def resolve(self, system: str, user_id: str) -> str:
        """
        Returns canonical user ID across systems.
        """

        key = f"{system}:{user_id}"

        if key in self.identity_map:
            return self.identity_map[key]

        canonical_id = self._generate_canonical_id(system, user_id)
        self.identity_map[key] = canonical_id

        return canonical_id

    def _generate_canonical_id(self, system: str, user_id: str) -> str:
        """
        MVP strategy:
        deterministic but system-aware identity mapping
        """
        return f"user::{user_id}"

    def link_identities(self, system_a: str, user_a: str, system_b: str, user_b: str):
        """
        Manually link identities across systems (future admin feature)
        """
        canonical = self.resolve(system_a, user_a)
        self.identity_map[f"{system_b}:{user_b}"] = canonical