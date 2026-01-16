"""VK utilities for peer_id/chat_id conversion and mention parsing."""

import re
from typing import Optional

MENTION_PATTERN = re.compile(r'^\[club\d+\|@[^]]+\]\s*', re.IGNORECASE)


def peer_id_to_chat_id(peer_id: int) -> int:
    """
    Конвертирует peer_id в chat_id для бесед.

    Для бесед: chat_id = peer_id - 2000000000
    Для личных сообщений: возвращает peer_id как есть

    Args:
        peer_id: Peer ID из VK API

    Returns:
        Chat ID для использования в messages.send
    """
    if peer_id > 2000000000:
        return peer_id - 2000000000
    return peer_id


def is_mention(msg: str) -> bool:
    """
    Проверяет, содержит ли сообщение упоминание бота.

    Args:
        msg: Текст сообщения

    Returns:
        True если сообщение содержит упоминание бота
    """
    return delete_mention_text(msg) != msg


def delete_mention_text(msg: str) -> str:
    """
    Удаляет упоминание бота из начала сообщения.

    Args:
        msg: Текст сообщения с упоминанием

    Returns:
        Текст без упоминания
    """
    return MENTION_PATTERN.sub('', msg)

