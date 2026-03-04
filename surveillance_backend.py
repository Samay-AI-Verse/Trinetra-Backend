from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(
    title="Trinetra Drone Surveillance Backend",
    description="Backend for handling AI-based drone surveillance alerts including Crowd, Riot, and Suspicious Activities.",
    version="1.0.0",
)

# --- MODELS ---


class Detection(BaseModel):
    label: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]


class SurveillanceAlert(BaseModel):
    alert_type: str  # "CROWD", "HUMAN", "RIOT", "WEAPON", "SUSPICIOUS_ACTIVITY"
    count: int
    message: str
    timestamp: datetime = datetime.now()
    detections: Optional[List[Detection]] = None
    location: Optional[str] = "Unknown"


# --- ENDPOINTS ---


@app.get("/")
async def root():
    return {"status": "Trinetra Surveillance Online", "version": "1.0.0"}


@app.post("/api/surveillance/alert")
async def receive_alert(alert: SurveillanceAlert):
    """
    General endpoint for any surveillance alert from the drone.
    """
    print(
        f"[{alert.timestamp}] ALERT: {alert.alert_type} - {alert.message} (Count: {alert.count})"
    )
    # Here you would typically save to DB or send push notifications to officers
    return {"status": "Alert Received", "alert_id": alert.alert_type}


@app.post("/api/surveillance/crowd")
async def crowd_alert(alert: SurveillanceAlert):
    """
    Dedicated endpoint for Crowd and Riot alerts.
    """
    if alert.count > 10:
        alert.message = f"!!! MASSIVE CROWD DETECTED !!! {alert.count} people."
    print(f"CRITICAL: {alert.message}")
    return {"status": "Crowd Alert Processed"}


@app.post("/api/surveillance/suspicious")
async def suspicious_activity(alert: SurveillanceAlert):
    """
    Endpoint for suspicious hand-exchange or aggressive behavior.
    """
    print(f"INVESTIGATION REQUIRED: {alert.message}")
    return {"status": "Suspicious Activity Logged"}


@app.post("/api/surveillance/weapon")
async def weapon_detection(alert: SurveillanceAlert):
    """
    Endpoint for weapon detection alerts.
    """
    print(f"!!! ARMED THREAT DETECTED !!!: {alert.message}")
    return {"status": "Weapon Alert Dispatched"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
