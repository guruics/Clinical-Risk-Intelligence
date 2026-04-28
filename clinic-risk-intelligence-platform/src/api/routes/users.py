# User API routes
from fastapi import APIRouter

router = APIRouter()


USER_EVENTS = {}


@router.get("/{user_id}/risk")
def get_user_risk(user_id: str):

    events = USER_EVENTS.get(user_id, [])

    if not events:
        return {
            "user_id": user_id,
            "risk_score": 0
        }

    avg = sum(e["risk_score"] for e in events) / len(events)

    return {
        "user_id": user_id,
        "risk_score": round(avg, 2),
        "event_count": len(events)
    }