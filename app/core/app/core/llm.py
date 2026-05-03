import anthropic
import openai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def get_ai_response(messages: list, system: str = "") -> str:
    if settings.LLM_PROVIDER == "claude":
        client = anthropic.AsyncAnthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )
        response = await client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=system or "You are NEXUS, a helpful AI assistant.",
            messages=messages,
        )
        return response.content[0].text

    elif settings.LLM_PROVIDER == "openai":
        client = openai.AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )
        all_messages = [{"role": "system", "content": system}]
        all_messages.extend(messages)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=all_messages,
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")
