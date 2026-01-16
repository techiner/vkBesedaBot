"""Event dispatcher for routing VK events."""

from vk_api.bot_longpoll import VkBotEventType
from bot.handlers.message_handler import handle_message
from bot.handlers.errors import handle_error


def dispatch_event(vk, event) -> None:
    """
    Dispatch VK event to appropriate handler.

    Args:
        vk: VK API session
        event: VK bot event
    """
    try:
        if event.type == VkBotEventType.MESSAGE_NEW:
            handle_message(vk, event)
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            # Можно добавить обработку ответов на сообщения
            pass
        # Добавить другие типы событий по необходимости
    except Exception as e:
        handle_error(e, "при диспетчеризации события")

