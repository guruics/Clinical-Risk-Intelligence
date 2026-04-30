def run_athena_risk_pipeline():
    from src.connectors.athena.auth import AthenaAuth
    from src.connectors.athena.client import AthenaClient
    from src.engine.rule_engine import RuleEngine
    from src.engine.risk_scoring import RiskScoringEngine
    from src.normalization.athena_event_mapper import AthenaEventMapper 
    from src.state.risk_state import LATEST_FINDINGS

    auth = AthenaAuth()
    token = auth.get_token()

    client = AthenaClient(token)
    # events = client.fetch_patient_events()

    patients = client.get_patients("Smith")
    # events = AthenaEventMapper.from_patients(patients)

    mapper = AthenaEventMapper()
    events = mapper.map_patient_search_response(
        {"patients": patients}
    )


    rule_engine = RuleEngine()
    scoring_engine = RiskScoringEngine()

    all_findings = []
    
    all_findings = [{
    "rule_name": "Demo PHI Access",
    "category": "PHI_ACCESS",
    "severity": "HIGH",
    "event_id": "test-1"
    }]

    for event in events:
        findings = rule_engine.evaluate(event)
        if findings:
            all_findings.extend(findings)

    summary = scoring_engine.calculate_score(all_findings)

    print("\n--- RISK FINDINGS ---")
    print("Total events:", len(events))
    print("Total findings:", len(all_findings))

    LATEST_FINDINGS.clear()
    LATEST_FINDINGS.extend(all_findings)

    return {
    "events": events,
    "findings": all_findings,
    "risk_summary": summary
    }
    # return result