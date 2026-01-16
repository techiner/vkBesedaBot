"""VK API client module."""

from bot.vk.client import VKClient
from bot.vk.sender import send_message
from bot.vk.utils import peer_id_to_chat_id, is_mention, delete_mention_text

__all__ = ['VKClient', 'send_message', 'peer_id_to_chat_id', 'is_mention', 'delete_mention_text']

