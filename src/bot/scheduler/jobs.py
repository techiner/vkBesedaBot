"""Scheduled jobs definitions."""

from itertools import islice
import csv
import random
from bot.vk.sender import send_message
from bot.vk.utils import peer_id_to_chat_id
from bot.services.subscription_service import get_subscribers
from bot.services.ai_service import get_quote
from bot.config.settings import settings
from bot.config.logging import get_logger

logger = get_logger(__name__)


def job_jokes(vk) -> None:
    """Job for sending jokes to subscribers at 9:00."""
    logger.info("Запуск задания: рассылка шуток")
    path = settings.JOKES_CSV
    jokes_count = 2
    jokes_indexes = random.sample(range(1, 1000), jokes_count)
    jokes_msgs = []

    for row_index in jokes_indexes:
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Считываем заголовок
                row = next(islice(reader, row_index-1, row_index), None)
                if row:
                    jokes_msgs.append(row[0])
        except Exception as e:
            logger.error(f"Error reading joke from CSV: {e}")

    subscribers = get_subscribers()
    logger.info(f"Выбранные шутки для отправки ({len(subscribers)} подписчиков)")

    for peer_id in subscribers:
        chat_id = peer_id_to_chat_id(peer_id)
        send_message(vk, chat_id, "[🤭 Шутка-минутка]")
        for msg in jokes_msgs:
            send_message(vk, chat_id, msg)
            logger.debug(f"[{peer_id} -> chat {chat_id}] {msg}")


def job_quote(vk) -> None:
    """Job for sending quotes to subscribers at 20:00."""
    logger.info("Запуск задания: рассылка цитат")
    subscribers = get_subscribers()
    logger.info(f"Цитаты для отправки ({len(subscribers)} подписчиков)")

    quote = get_quote()

    for peer_id in subscribers:
        chat_id = peer_id_to_chat_id(peer_id)
        send_message(vk, chat_id, "[💭 Цитата дня]")
        send_message(vk, chat_id, quote)

