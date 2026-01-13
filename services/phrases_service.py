

import re

from infra import phrases_store_service


def find_phrase(text: str) -> str | None:
    """Поиск фразы без учета регистра"""
    phrase_database = phrases_store_service.load_phrases()
    res = []
    for key, value in phrase_database.items():
        pattern = r'(?<!\w)' + re.escape(key) + r'(?!\w)'
        if re.search(pattern, text, flags=re.IGNORECASE):
            res.append(value)

    if len(res) > 0:
        return " ".join(res)
    return None