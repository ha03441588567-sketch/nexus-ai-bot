from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from handlers.chat import (
    handle_start, handle_chat, 
    handle_price, handle_signal,
    handle_support, handle_reset
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NEXUS AI Bot")

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
    
    msg = update.get("message", {})
    if not msg:
        return {"ok": True}
    
    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    name = msg["from"].get("first_name", "User")
    text = msg.get("text", "")
    
    if text == "/start":
        await handle_start(chat_id, name)
    elif text.startswith("/price "):
        coin = text.split(" ")[1]
        await handle_price(chat_id, coin)
    elif text.startswith("/signal "):
        coin = text.split(" ")[1]
        await handle_signal(chat_id, coin)
    elif text.startswith("/support "):
        issue = text[9:]
        await handle_support(chat_id, user_id, issue)
    elif text == "/reset":
        await handle_reset(chat_id, user_id)
    elif text.startswith("/ask "):
        question = text[5:]
        await handle_chat(chat_id, user_id, question)
    else:
        await handle_chat(chat_id, user_id, text)
    
    return {"ok": True}
