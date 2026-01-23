"""Scheduled jobs definitions."""

from bot.vk.sender import send_message
from bot.vk.utils import peer_id_to_chat_id
from bot.services.subscription_service import get_subscribers
from bot.services.ai_service import get_quote
from bot.config.logging import get_logger

logger = get_logger(__name__)


def job_quote(vk) -> None:
    """Job for sending quotes to subscribers at 20:00."""
    logger.info("Запуск задания: рассылка цитат")
    subscribers = get_subscribers("цитаты")
    logger.info(f"Цитаты для отправки ({len(subscribers)} подписчиков)")

    quote = get_quote()

    for peer_id in subscribers:
        chat_id = peer_id_to_chat_id(peer_id)
        send_message(vk, chat_id, "[💭 Цитата дня]")
        send_message(vk, chat_id, quote)

