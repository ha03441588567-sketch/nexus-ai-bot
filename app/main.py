from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

async def send(chat_id, text):
    async with httpx.AsyncClient() as c:
        await c.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

async def ask_claude(text):
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
            json={"model": "claude-haiku-4-5-20251001", "max_tokens": 500, "messages": [{"role": "user", "content": text}]}
        )
        return r.json()["content"][0]["text"]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook/telegram")
async def webhook(request: Request):
    data = await request.json()
    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text", "")
    if not chat_id or not text:
        return {"ok": True}
    if text == "/start":
        await send(chat_id, "👋 Salam! Main NEXUS AI Bot hun! Kuch bhi pucho!")
    else:
        reply = await ask_claude(text)
        await send(chat_id, reply)
    return {"ok": True}
