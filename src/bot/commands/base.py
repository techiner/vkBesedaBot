"""Base command interface and command enum."""

from enum import Enum
from abc import ABC, abstractmethod


class Commands(str, Enum):
    """Available bot commands."""

    HELP = 'help'
    PROMPT = 'окейалеша'
    SUBSCRIBE = 'подписаться'
    ANALYZE = 'анализ'


class Command(ABC):
    """Base command interface."""

    @abstractmethod
    def execute(self, vk, chat_id: int, peer_id: int, args: str) -> None:
        """
        Execute the command.

        Args:
            vk: VK API session
            chat_id: Chat ID
            peer_id: Peer ID
            args: Command arguments
        """
        pass

