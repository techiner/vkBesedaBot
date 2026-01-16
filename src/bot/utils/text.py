"""Text parsing and processing utilities."""

import shlex
from bot.commands.base import Commands


def get_command(msg: str) -> Commands | None:
    """
    Извлекает команду из сообщения с упоминанием.

    Args:
        msg: Текст сообщения (уже без упоминания)

    Returns:
        Команда или None, если команда не найдена
    """
    shlexed = shlex.split(msg.strip())
    if len(shlexed) > 0:
        try:
            return Commands(shlexed[0])
        except ValueError:
            pass
    return None


def get_args_from_command(msg: str) -> str:
    """
    Извлекает аргументы команды из сообщения.

    Args:
        msg: Текст сообщения (уже без упоминания)

    Returns:
        Аргументы команды как строка
    """
    shlexed = shlex.split(msg.strip())
    if len(shlexed) > 1:
        return " ".join(shlexed[1:])
    return ""

