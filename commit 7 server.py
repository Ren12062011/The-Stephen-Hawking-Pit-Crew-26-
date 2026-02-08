# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from shared import trigger, CONFIG, HISTORY, user_login, register_device

import base64
from fastapi.responses import JSONResponse


app = FastAPI(title="Assistive Buttons Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TriggerRequest(BaseModel):
    button: str
    language: str = "en" 
    custom_text: str = None  
    device_id: str = "unknown"  
    user_id: str = "default"
    device_name: str = None  

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/trigger")
def trigger_endpoint(req: TriggerRequest):
    
    if req.device_name and req.user_id != "default":
        try:
            register_device(req.user_id, req.device_id, req.device_name)
        except Exception:
            pass
    
    evt = trigger(
        button=req.button,
        language=req.language,
        source="DEVICE",
        custom_text=req.custom_text,
        device_id=req.device_id,
        user_id=req.user_id
        
        )
    
    audio_bytes = evt.get("audio")

    audio_b64 = None
    if audio_bytes:
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    
    return {
        "ok": True,
        "event": evt,
        "audio_base64": audio_b64
    }


@app.get("/config")
def get_config():
    return CONFIG

@app.get("/history")
def get_history():
    return HISTORY

@app.post("/register_device")
def register_device_endpoint(req: Dict[str, Any]):
    """Register a physical device (e.g., ESP32)."""
    device_id = req.get("device_id")
    device_name = req.get("device_name")
    user_id = req.get("user_id")
    device_type = req.get("device_type", "unknown")
    pin_mapping = req.get("pin_mapping", {})
    
    try:
        register_device(user_id, device_id, device_name)
        return {
            "ok": True,
            "device_id": device_id,
            "device_name": device_name,
            "message": f"Device '{device_name}' registered successfully"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}