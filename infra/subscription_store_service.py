import json
import os
from typing import List


SUBSCRIPTION_FILE = os.path.join("data", "comedy_subscription.json")


def load_subscriptions() -> List[int]:
    """
    Загружает список peer_id, подписанных на рассылку шуток.
    При отсутствии файла или ошибке чтения возвращает пустой список.
    """
    if not os.path.exists(SUBSCRIPTION_FILE):
        return []

    try:
        with open(SUBSCRIPTION_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if isinstance(data, list):
                # Фильтруем и приводим к int
                return [int(x) for x in data if isinstance(x, (int, str))]
            return []
    except (OSError, json.JSONDecodeError, ValueError):
        # В случае любой ошибки не ломаем бота, просто считаем, что подписок нет
        return []


def save_subscriptions(subs: List[int]) -> None:
    """
    Сохраняет список peer_id, подписанных на рассылку шуток.
    """
    # Убедимся, что каталог существует
    os.makedirs(os.path.dirname(SUBSCRIPTION_FILE), exist_ok=True)

    # Приводим к уникальному списку int
    unique_subs = sorted({int(x) for x in subs})

    with open(SUBSCRIPTION_FILE, "w", encoding="utf-8") as f:
        json.dump(unique_subs, f, ensure_ascii=False, indent=2)


