import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def handle_chat(chat_id: int, user_id: int, text: str):
    await send_typing(chat_id)
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": text}]
    )
    
    reply = response.content[0].text
    await send_message(chat_id, reply)
