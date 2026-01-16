"""Application settings and configuration."""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # VK API settings
    VK_TOKEN: str = os.getenv("TOKEN", "")
    GROUP_ID: int = int(os.getenv("GROUP_ID", "0"))

    # AI Service settings
    NEUROAPI_API_KEY: str = os.getenv("NEUROAPI_API_KEY", "")

    # Data paths
    DATA_DIR: str = "data"
    PHRASES_FILE: str = os.path.join(DATA_DIR, "phrases.json")
    SUBSCRIPTIONS_FILE: str = os.path.join(DATA_DIR, "comedy_subscription.json")
    JOKES_CSV: str = os.path.join(DATA_DIR, "clean_comedy_gold_ru.csv")
    DB_PATH: str = os.path.join(DATA_DIR, "bot.db")

    @classmethod
    def validate(cls) -> None:
        """Validate that required settings are set."""
        if not cls.VK_TOKEN:
            raise ValueError("TOKEN environment variable is required")
        if not cls.GROUP_ID:
            raise ValueError("GROUP_ID environment variable is required")


# Глобальный экземпляр настроек
settings = Settings()

