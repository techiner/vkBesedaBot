"""Error handling utilities."""

import logging
from bot.config.logging import get_logger

logger = get_logger(__name__)


def handle_error(error: Exception, context: str = "") -> None:
    """
    Handle and log errors.

    Args:
        error: Exception that occurred
        context: Additional context about where error occurred
    """
    error_msg = f"Ошибка {context}: {error}"
    logger.error(error_msg, exc_info=True)

