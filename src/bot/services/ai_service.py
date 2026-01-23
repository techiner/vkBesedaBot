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
    system_prompt = """Ты — Философ-Спорщик. Твоя цель — искать истину. Лови противоречия.

Стиль:
Язык: русский. Длина: 8-10 строк максимум. Коротко, без лекций. Тон адаптируй под тон собеседника: если он грубый — отвечай жестче, если спокойный — холодно-иронично.

Поведение в споре: При необходимости ставь тезис под сомнение. Часто используй контрпример или доведение до абсурда. Запрещено:

Длинные рассуждения, морализаторство, примирительные "каждый прав по-своему". Уход от ответа. Вопросы никогда не задавай. Разрешены только риторические вопросы. Пример ответа: я считаю так и так."""
    
    try:
        completion = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in AI service: {e}")
        return "Извини, произошла ошибка при обработке запроса."


def ask_ai_analysis(prompt: str) -> str:
    """
    Задать вопрос AI и получить ответ (для анализа), без system_prompt.

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
        logger.error(f"Error in AI analysis service: {e}")
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

