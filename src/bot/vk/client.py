"""VK API client and longpoll setup."""

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
from bot.config.settings import settings
from bot.config.logging import get_logger

logger = get_logger(__name__)


class VKClient:
    """VK API client wrapper."""

    def __init__(self):
        """Initialize VK client with settings."""
        settings.validate()
        self.session = vk_api.VkApi(token=settings.VK_TOKEN)
        self.longpoll = VkBotLongPoll(self.session, settings.GROUP_ID)
        logger.info("VK client initialized")

    @property
    def api(self):
        """Get VK API session."""
        return self.session

    def listen(self):
        """Start listening to longpoll events."""
        logger.info("Starting longpoll listener")
        return self.longpoll.listen()

