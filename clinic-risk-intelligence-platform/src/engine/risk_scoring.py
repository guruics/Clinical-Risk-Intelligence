from typing import List, Dict, Any


class RiskScoringEngine:
    """
    Converts RuleEngine findings into a normalized risk score (0–100)
    """

    CATEGORY_WEIGHTS = {
        "PHI_ACCESS": 1.0,
        "CLINICAL": 1.3,
        "BILLING": 1.5,
        "BEHAVIORAL": 0.9
    }

    SEVERITY_MAP = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 4,
        "CRITICAL": 5
    }

    def calculate_score(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_score = 0
        breakdown = []

        for f in findings:
            category = f.get("category", "BEHAVIORAL")
            severity_label = f.get("severity", "MEDIUM")

            severity = self.SEVERITY_MAP.get(severity_label.upper(), 2)
            weight = self.CATEGORY_WEIGHTS.get(category.upper(), 1.0)

            score = severity * weight * 10  # scaling factor

            total_score += score

            breakdown.append({
                "rule": f.get("rule_name"),
                "category": category,
                "severity": severity_label,
                "weighted_score": score,
                "event_id": f.get("event_id")
            })

        # Normalize to 0–100 scale
        normalized_score = min(100, total_score)

        return {
            "risk_score": round(normalized_score, 2),
            "total_raw_score": total_score,
            "breakdown": breakdown,
            "risk_level": self._classify(normalized_score)
        }

    def _classify(self, score: float) -> str:
        if score < 20:
            return "LOW"
        elif score < 50:
            return "MODERATE"
        elif score < 75:
            return "HIGH"
        return "CRITICAL"