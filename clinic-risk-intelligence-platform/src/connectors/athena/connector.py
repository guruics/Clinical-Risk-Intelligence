from src.connectors.athena.client import AthenaClient
from src.connectors.athena.mapper import AthenaMapper
from src.connectors.athena.router import AthenaPracticeRouter

from src.engine.rule_engine import RuleEngine


class AthenaConnector:

    def __init__(self, config, rule_engine: RuleEngine):
        self.client = AthenaClient(config)
        self.mapper = AthenaMapper()
        self.router = AthenaPracticeRouter()
        self.engine = rule_engine


    def sync_patients(self, context: dict):

        practice_id = self.router.resolve(context)

        data = self.client.get_patients(practice_id=practice_id)

        results = []

        for p in data.get("patients", []):

            event = self.mapper.map_patient_access(p)

            # inject practice context (IMPORTANT)
            event.metadata["practice_id"] = practice_id

            findings = self.engine.evaluate(event)

            results.append({
                "practice_id": practice_id,
                "event": event,
                "risk_flags": findings
            })

        return results