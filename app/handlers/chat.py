import logging
import anthropic
import os
from app.services.telegram import send_message, send_typing

logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def handle_start(chat_id: int, name: str):
    text = f"Welcome {name}! I am NEXUS AI Bot!"
    await send_message(chat_id, text)

async def handle_chat(chat_id: int, user_id: int, text: str):
    await send_typing(chat_id)
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": text}]
    )
    reply = response.content[0].text
    await send_message(chat_id, reply)

async def handle_price(chat_id: int, coin: str):
    await send_message(chat_id, f"Price feature coming soon for {coin}!")

async def handle_signal(chat_id: int, coin: str):
    await send_message(chat_id, f"Signal feature coming soon for {coin}!")

async def handle_support(chat_id: int, user_id: int, issue: str):
    await send_message(chat_id, f"Support: {issue}")

async def handle_reset(chat_id: int, user_id: int):
    await send_message(chat_id, "Chat cleared!")
