from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NEXUS AI Bot",
    description="AI Automation Bot for Telegram and WhatsApp",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    update = await request.json()
    logger.info(f"Update received: {update}")
    return {"ok": True}
