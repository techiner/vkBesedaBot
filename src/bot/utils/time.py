"""Time utilities."""

from datetime import datetime
from typing import Optional


def format_datetime(dt: Optional[datetime] = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Форматирует datetime в строку.

    Args:
        dt: Datetime объект (по умолчанию текущее время)
        format_str: Формат строки

    Returns:
        Отформатированная строка
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(format_str)

