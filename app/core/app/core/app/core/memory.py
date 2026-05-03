import json
import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def get_redis():
    return redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_history(user_id: int) -> list:
    try:
        r = await get_redis()
        raw = await r.get(f"chat:{user_id}")
        if not raw:
            return []
        return json.loads(raw)
    except Exception as e:
        logger.warning(f"Redis error: {e}")
        return []

async def save_message(user_id: int, role: str, content: str):
    try:
        r = await get_redis()
        history = await get_history(user_id)
        history.append({"role": role, "content": content})
        history = history[-20:]
        await r.setex(f"chat:{user_id}", 3600, json.dumps(history))
    except Exception as e:
        logger.warning(f"Redis save error: {e}")

async def clear_history(user_id: int):
    try:
        r = await get_redis()
        await r.delete(f"chat:{user_id}")
    except Exception as e:
        logger.warning(f"Redis clear error: {e}")
