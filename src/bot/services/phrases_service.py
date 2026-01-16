"""Phrases service for finding trigger phrases."""

import random
import re
from typing import Optional
from bot.storage.db_store import PhrasesStore


def find_phrase(text: str) -> Optional[str]:
    """
    Поиск фразы в тексте без учета регистра.

    Args:
        text: Текст для поиска

    Returns:
        Один случайный ответ на каждую найденную фразу,
        объединённые в одну строку, либо None
    """
    store = PhrasesStore()
    phrase_database = store.load_phrases()  # Dict[str, List[str]]
    res: list[str] = []

    for key, responses in phrase_database.items():
        if not responses:
            continue

        pattern = r'(?<!\w)' + re.escape(key) + r'(?!\w)'
        if re.search(pattern, text, flags=re.IGNORECASE):
            # Для каждой совпавшей фразы выбираем один случайный ответ
            res.append(random.choice(responses))

    if res:
        return " ".join(res)
    return None
