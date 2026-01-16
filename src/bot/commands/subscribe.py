"""Subscribe command handler."""

import shlex
from bot.vk.sender import send_message
from bot.storage.db_store import SubscriptionsStore


def handle_subscribe(vk, chat_id: int, peer_id: int, args_text: str) -> None:
    """
    Handle subscribe command.

    Args:
        vk: VK API session
        chat_id: Chat ID
        peer_id: Peer ID
        args_text: Command arguments
    """
    parts = shlex.split(args_text.strip())

    if len(parts) != 1 or parts[0].lower() != "шутки":
        send_message(
            vk,
            chat_id,
            'Неправильно! Используй: подписаться "шутки"',
        )
        return

    store = SubscriptionsStore()
    
    if store.add_subscription(peer_id, "шутки"):
        send_message(vk, chat_id, "Подписал этот чат на ежедневные шутки 🤡")
    else:
        send_message(vk, chat_id, "Ты уже подписан на мои шутки!")

