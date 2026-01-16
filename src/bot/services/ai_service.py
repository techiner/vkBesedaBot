"""AI service for generating responses."""

import os
from openai import OpenAI
from bot.config.settings import settings
from bot.config.logging import get_logger

logger = get_logger(__name__)

# Глобальный клиент (создаётся один раз)
client = OpenAI(
    base_url="https://neuroapi.host/v1",
    api_key=settings.NEUROAPI_API_KEY or os.getenv("NEUROAPI_API_KEY", ""),
)


def ask_ai(prompt: str) -> str:
    """
    Задать вопрос AI и получить ответ.

    Args:
        prompt: Текст запроса

    Returns:
        Ответ от AI
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in AI service: {e}")
        return "Извини, произошла ошибка при обработке запроса."


def get_quote() -> str:
    """
    Получить цитату от AI.

    Returns:
        Цитата с автором
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": "Напиши одну цитату о жизни и подпиши ее автора"}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error getting quote: {e}")
        return "Извини, не смог получить цитату."

