import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"

async def send_message(chat_id: int, text: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text[:4096],
                "parse_mode": "Markdown",
            },
        )
        return response.json()

async def send_typing(chat_id: int):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BASE_URL}/sendChatAction",
            json={
                "chat_id": chat_id,
                "action": "typing"
            },
        )

async def set_webhook(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/setWebhook",
            json={"url": url},
        )
        return response.json()
