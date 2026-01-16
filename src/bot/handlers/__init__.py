"""Event handlers module."""

from bot.handlers.dispatcher import dispatch_event
from bot.handlers.message_handler import handle_message
from bot.handlers.errors import handle_error

__all__ = ['dispatch_event', 'handle_message', 'handle_error']
