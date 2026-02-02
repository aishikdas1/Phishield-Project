from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="PhishShield API")

# Serve static files (HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Data model for scan requests
class Message(BaseModel):
    text: str

# Root: serve the web app
@app.get("/")
def serve_index():
    return FileResponse(os.path.join("static", "index.html"))

# Scan endpoint
@app.post("/scan")
def scan_message(message: Message):
    text = message.text.lower()
    score = 0
    reasons = []

    if "urgent" in text or "immediately" in text:
        score += 0.3
        reasons.append("Urgent language detected")

    if "http" in text or "www" in text:
        score += 0.4
        reasons.append("Suspicious link detected")

    if "password" in text or "verify" in text:
        score += 0.3
        reasons.append("Credential request detected")

    score = min(score, 1.0)

    return {
        "phishing_probability": round(score * 100, 2),
        "reasons": reasons
    }
