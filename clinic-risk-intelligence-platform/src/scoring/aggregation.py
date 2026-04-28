# Score aggregation
from typing import List, Dict


class RiskAggregator:
    """
    Aggregates event-level risk into user and clinic-level scores.
    """

    def aggregate_user_risk(self, scored_events: List[Dict]) -> float:
        if not scored_events:
            return 0.0

        total = sum(e.get("risk_score", 0) for e in scored_events)
        return min(total / len(scored_events), 100.0)

    def aggregate_clinic_risk(self, user_scores: List[float]) -> float:
        if not user_scores:
            return 0.0

        # weighted exposure model (simple MVP)
        return min(sum(user_scores) / len(user_scores), 100.0)

    def risk_trend(self, historical_scores: List[float]) -> str:
        if len(historical_scores) < 2:
            return "STABLE"

        if historical_scores[-1] > historical_scores[-2]:
            return "INCREASING"
        elif historical_scores[-1] < historical_scores[-2]:
            return "DECREASING"

        return "STABLE"