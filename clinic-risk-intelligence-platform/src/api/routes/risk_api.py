from fastapi import FastAPI
from src.engine.risk_scoring import RiskScoringEngine
from src.pipeline.athena_pipeline import run_athena_risk_pipeline

from src.state.risk_state import LATEST_FINDINGS


app = FastAPI()

scorer = RiskScoringEngine()
 print("I am in risk_API")
# In-memory placeholder (replace later with DB)
# LATEST_FINDINGS = []


@app.get("/risk/summary")
def get_risk_summary():
    result = scorer.calculate_score(LATEST_FINDINGS)

    return {
        "risk_score": result["risk_score"],
        "risk_level": result["risk_level"],
        "breakdown": result["breakdown"]
    }


@app.post("/risk/update")
def update_findings(findings: list):
    global LATEST_FINDINGS
    LATEST_FINDINGS = findings
    return {"status": "updated", "count": len(findings)}

@app.get("/risk/run")
def run_risk():
    return run_athena_risk_pipeline()
