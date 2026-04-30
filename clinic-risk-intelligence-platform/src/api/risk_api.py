from fastapi import FastAPI
from src.engine.risk_scoring import RiskScoringEngine
from fastapi.middleware.cors import CORSMiddleware
from src.pipeline.athena_pipeline import run_athena_risk_pipeline

from src.state.risk_state import LATEST_FINDINGS


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite
        "http://localhost:3000"   # CRA (optional)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scorer = RiskScoringEngine()





@app.get("/risk/summary")
def get_risk_summary():
    print("Total findings in risk_api:", len(LATEST_FINDINGS))
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

@app.post("/risk/run")
def run_risk():
    result =  run_athena_risk_pipeline()
    LATEST_FINDINGS.clear()
    LATEST_FINDINGS.extend(result["findings"])
    return result