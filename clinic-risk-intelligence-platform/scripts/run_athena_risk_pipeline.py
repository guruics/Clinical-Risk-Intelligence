import requests

from src.connectors.athena.auth import AthenaAuth
from src.connectors.athena.config import ATHENA_BASE_URL, practice_id
from src.normalization.athena_event_mapper import AthenaEventMapper

from src.engine.rule_engine import RuleEngine

# Import rules
from src.engine.rules.access_rules import UnauthorizedPHIAccessRule, AfterHoursAccessRule
from src.engine.rules.billing_rules import BillingWithoutEncounterRule
from src.engine.rules.clinical_pattern_rules import PrescriptionSpikeRule
from src.engine.risk_scoring import RiskScoringEngine

from src.state.risk_state import LATEST_FINDINGS



def build_rule_engine():
    engine = RuleEngine()

    # Register core rules
    engine.register_rule(UnauthorizedPHIAccessRule())
    engine.register_rule(AfterHoursAccessRule())
    engine.register_rule(BillingWithoutEncounterRule())
    engine.register_rule(PrescriptionSpikeRule())

    return engine


def fetch_athena_patients(token: str):
    url = f"{ATHENA_BASE_URL}/v1/{practice_id}/patients/search"

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }

    params = {"searchterm": "smith"}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()


def main():
    # 1. Auth
    auth = AthenaAuth()
    token = auth.get_token()

    # 2. Fetch data
    raw_response = fetch_athena_patients(token)

    print("Fetched patients:", len(raw_response.get("patients", [])))

    # 3. Map to UnifiedEvent
    mapper = AthenaEventMapper()
    events = mapper.map_patient_search_response(raw_response)

    print("UnifiedEvents created:", len(events))

    # 4. Rule Engine
    engine = build_rule_engine()

    # all_findings = []

    all_findings = [{
    "rule_name": "Demo PHI Access",
    "category": "PHI_ACCESS",
    "severity": "HIGH",
    "event_id": "test-1"
    }]

    LATEST_FINDINGS.clear()
    LATEST_FINDINGS.extend(all_findings)

    for event in events:
        findings = engine.evaluate(event)
        all_findings.extend(findings)

    # 5. Output Risk Findings
    print("\n--- RISK FINDINGS ---")
    print("Total events:", len(events))
    print("Total findings:", len(all_findings))

    for f in all_findings[:10]:
        print(f)

    # after rule evaluation
    scoring_engine = RiskScoringEngine()
    risk_result = scoring_engine.calculate_score(all_findings)

    print("\n--- RISK SCORE SUMMARY ---")
    print("Risk Score:", risk_result["risk_score"])
    print("Risk Level:", risk_result["risk_level"])

    print("\nTop Drivers:")
    for b in risk_result["breakdown"][:5]:
        print(b)


if __name__ == "__main__":
    main()