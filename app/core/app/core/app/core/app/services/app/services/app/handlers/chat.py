from app.core.llm import get_ai_response
from app.core.memory import get_history, save_message, clear_history
from app.services.telegram import send_message, send_typing
from app.services.trading import get_price, get_signal
import logging

logger = logging.getLogger(__name__)

async def handle_start(chat_id: int, name: str):
    text = f"""
👋 *Welcome {name}!*

I am NEXUS AI Bot!

*Commands:*
/ask - Chat with AI
/price BTC - Crypto price
/signal ETH - Trading signal
/support - Customer support
/reset - Clear chat history
"""
    await send_message(chat_id, text)

async def handle_chat(chat_id: int, user_id: int, text: str):
    await send_typing(chat_id)
    history = await get_history(user_id)
    await save_message(user_id, "user", text)
    messages = history + [{"role": "user", "content": text}]
    reply = await get_ai_response(messages)
    await save_message(user_id, "assistant", reply)
    await send_message(chat_id, reply)

async def handle_price(chat_id: int, coin: str):
    if not coin:
        await send_message(chat_id, "Usage: /price BTC")
        return
    await send_typing(chat_id)
    try:
        data = await get_price(coin)
        icon = "🟢" if data["change_24h"] > 0 else "🔴"
        text = f"""
💰 *{data['name']} ({data['symbol']})*

Price: `${data['price']:,.2f}`
{icon} 24h: `{data['change_24h']:+.2f}%`
Market Cap: `${data['market_cap']/1e9:.2f}B`
"""
        await send_message(chat_id, text)
    except Exception:
        await send_message(chat_id, "❌ Coin not found. Try BTC, ETH, SOL")

async def handle_signal(chat_id: int, coin: str):
    if not coin:
        await send_message(chat_id, "Usage: /signal BTC")
        return
    await send_typing(chat_id)
    await send_message(chat_id, f"⏳ Analyzing {coin.upper()}...")
    try:
        data = await get_signal(coin)
        text = f"""
📊 *{data['name']} Signal*

Price: `${data['price']:,.2f}`
RSI: `{data['rsi']}`
Signal: *{data['signal']}*

⚠️ Not financial advice!
"""
        await send_message(chat_id, text)
    except Exception:
        await send_message(chat_id, "❌ Could not analyze. Try again.")

async def handle_support(chat_id: int, user_id: int, issue: str):
    await send_typing(chat_id)
    if not issue:
        await send_message(chat_id, "🎧 Please describe your issue and I will help!")
        return
    messages = [{"role": "user", "content": issue}]
    system = "You are a helpful customer support agent. Be friendly and solution focused."
    reply = await get_ai_response(messages, system=system)
    await send_message(chat_id, f"🎧 *Support:*\n\n{reply}")

async def handle_reset(chat_id: int, user_id: int):
    await clear_history(user_id)
    await send_message(chat_id, "🗑 Chat cleared! Starting fresh!")
