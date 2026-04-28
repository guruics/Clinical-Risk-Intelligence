# Risk scoring logic
from typing import List, Dict


class RiskCalculator:
    """
    Converts rule findings into weighted risk scores.
    """

    def __init__(self, weights: Dict[str, float]):
        """
        weights example:
        {
            "ACCESS": 0.3,
            "BILLING": 0.3,
            "WORKFLOW": 0.2,
            "CLINICAL": 0.2
        }
        """
        self.weights = weights

    def calculate_event_score(self, findings: List[Dict]) -> float:
        """
        Score a single event based on rule findings.
        """

        score = 0.0

        for f in findings:
            severity = f.get("severity", "LOW")
            domain = self._infer_domain(f)

            base_score = self._severity_to_score(severity)
            weight = self.weights.get(domain, 0.1)

            score += base_score * weight

        return min(score, 100.0)

    def _severity_to_score(self, severity: str) -> float:
        mapping = {
            "LOW": 10,
            "MEDIUM": 25,
            "HIGH": 60,
            "CRITICAL": 100
        }
        return mapping.get(severity, 0)

    def _infer_domain(self, finding: Dict) -> str:
        rule = finding.get("rule", "")

        if "BILL" in rule:
            return "BILLING"
        if "PHI" in rule or "ACCESS" in rule:
            return "ACCESS"
        if "LOGIN" in rule or "WORKFLOW" in rule:
            return "WORKFLOW"

        return "CLINICAL"
