from statistics import mode


def run_athena_risk_pipeline(mode, searchterm=None):
    from src.connectors.athena.auth import AthenaAuth
    from src.connectors.athena.client import AthenaClient
    from src.engine.rule_engine import RuleEngine
    from src.engine.risk_scoring import RiskScoringEngine
    from src.normalization.athena_event_mapper import AthenaEventMapper
    from src.state.risk_state import LATEST_FINDINGS
    from src.engine.rule_registry import RuleRegistry
    from collections import defaultdict

    # -----------------------------
    # AUTH + CLIENT
    # -----------------------------
    auth = AthenaAuth()
    token = auth.get_token()
    client = AthenaClient(token)

    # -----------------------------
    # DATA SOURCE
    # -----------------------------
    # if mode == "patients_search":
    #     patients = client.get_patients("Smith")
    # elif mode == "patients_search_all":
    #     patients = client.get_patients("")
    # elif mode == "patients_search_john":
    #     patients = client.get_patients(searchterm="John")
    # else:
    #     raise ValueError(f"Unsupported pipeline mode: {mode}")

    if mode == "patients_search":
    # Normalize input
        term = (searchterm or "").strip()

    # Athena requires a non-empty string
    if not term:
        term = "Smith"
        patients = client.get_patients(searchterm=term)
    else:
        raise ValueError(f"Unsupported pipeline mode: {mode}")

    # -----------------------------
    # EVENT MAPPING
    # -----------------------------
    mapper = AthenaEventMapper()
    events = mapper.map_patient_search_response({"patients": patients})

    # Ensure metadata
    for e in events:
        try:
            if hasattr(e, "metadata"):
                e.metadata["athena_api"] = "patients.search"
        except Exception:
            pass

    # =========================================================
    # 🔥 BUILD CONTEXT
    # =========================================================
    user_patient_counts = defaultdict(int)
    user_activity = defaultdict(list)

    normalized_events = []

    for e in events:
        normalized_events.append(e)

        try:
            user = getattr(e, "user_id", "unknown")
            resource = getattr(e, "resource_id", None)

            if resource:
                user_patient_counts[user] += 1
                user_activity[user].append(resource)

        except Exception:
            continue

    context = {
        "events": normalized_events,
        "user_activity": dict(user_activity),
        "user_patient_counts": dict(user_patient_counts)
    }

    # -----------------------------
    # RULE ENGINE
    # -----------------------------
    rule_engine = RuleEngine()
    scoring_engine = RiskScoringEngine()

    all_findings = []

    # =========================================================
    # 1. EVENT-LEVEL RULE EXECUTION
    # =========================================================
    for event in normalized_events:
        findings = rule_engine.evaluate(event, context)

        if not findings:
            continue

        if findings:
            # normalize → always extend list
            if isinstance(findings, list):
                all_findings.extend(findings)
            else:
                all_findings.append(findings)

  # =========================================================
# 2. BATCH / CONTEXT RULE EXECUTION
# =========================================================
    registry = RuleRegistry()
    batch_rules = registry.get_batch_rules()

    batch_findings = []
    events_by_user = defaultdict(list)

    # -----------------------------
    # Group events by user
    # -----------------------------
    for e in normalized_events:
        events_by_user[e.user_id].append(e)

    # -----------------------------
    # Execute batch rules per user
    # -----------------------------
    for rule in batch_rules:
        try:
            for user, user_events in events_by_user.items():

                # Build per-user context (IMPORTANT)
                user_context = {
                    "events": user_events,
                    "user_patient_counts": {
                        user: len(user_events)
                    },
                    "user_activity": {
                        user: [e.resource_id for e in user_events if e.resource_id]
                    }
                }

                result = rule.evaluate_batch(user_events, user_context)

                if not result:
                    continue

                # normalize dict
                if isinstance(result, dict):
                    result["user"] = user
                    batch_findings.append(result)

                # normalize list
                elif isinstance(result, list):
                    for r in result:
                        if isinstance(r, dict):
                            r["user"] = user
                            batch_findings.append(r)

        except Exception as e:
            print(f"[Batch Rule Error] {rule.__class__.__name__}: {e}")

    # -----------------------------
    # Merge batch findings
    # -----------------------------
    all_findings.extend(batch_findings)

    # =========================================================
    # 3. 🔥 DEDUPLICATION (CRITICAL FIX)
    # =========================================================
    unique = {}
    for f in all_findings:
        if not isinstance(f, dict):
            continue
        key = (
             f.get("rule_name"),
            f.get("event_id", "batch"),   # 🔥 FIX: batch-safe fallback
            f.get("user", f.get("category"))
        )
        unique[key] = f

    all_findings = list(unique.values())

    # -----------------------------
    # SCORING
    # -----------------------------
    summary = scoring_engine.calculate_score(all_findings)

    # -----------------------------
    # LOGGING
    # -----------------------------
    print("\n--- RISK FINDINGS ---")
    print("Total events:", len(normalized_events))
    print("Total findings (deduped):", len(all_findings))
    print("EVENT FINDINGS:", all_findings)
    print("BATCH FINDINGS:", batch_findings)

    # -----------------------------
    # STATE UPDATE
    # -----------------------------
    LATEST_FINDINGS.clear()
    LATEST_FINDINGS.extend(all_findings)

    # -----------------------------
    # RESPONSE
    # -----------------------------
    return {
        "events": normalized_events,
        "findings": all_findings,
        "risk_summary": summary
    }