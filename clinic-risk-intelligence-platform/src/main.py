# FastAPI entry point
from fastapi import FastAPI

from src.api.routes.risk import router as risk_router
from src.api.routes.events import router as events_router
from src.api.routes.users import router as users_router

app = FastAPI(
    title="Clinic Risk Intelligence Platform",
    version="0.1.0",
    description="Unified healthcare risk observability layer"
)

# Register routes
app.include_router(risk_router, prefix="/risk", tags=["Risk"])
app.include_router(events_router, prefix="/events", tags=["Events"])
app.include_router(users_router, prefix="/users", tags=["Users"])


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "clinic-risk-intelligence"
    }