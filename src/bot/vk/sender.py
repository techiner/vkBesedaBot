"""VK message sender module."""

import logging
from bot.config.logging import get_logger

logger = get_logger(__name__)


def send_message(vk, chat_id: int, text: str) -> None:
    """
    Отправляет сообщение в чат VK.

    Args:
        vk: VK API session
        chat_id: ID чата для отправки
        text: Текст сообщения
    """
    try:
        vk.method('messages.send', {
            'chat_id': chat_id,
            'message': text,
            'random_id': 0
        })
        logger.debug(f"Message sent to chat {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в chat {chat_id}: {e}")

