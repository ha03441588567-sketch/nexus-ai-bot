from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "NEXUS AI Bot"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "changeme"
    ADMIN_API_KEY: str = "changeme"

    TELEGRAM_BOT_TOKEN: str = ""
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    LLM_PROVIDER: str = "claude"

    REDIS_URL: str = "redis://localhost:6379"
    DATABASE_URL: str = "sqlite:///./nexus.db"

    WHATSAPP_TOKEN: str = ""
    BINANCE_API_KEY: str = ""
    BINANCE_SECRET: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
