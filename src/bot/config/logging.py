"""Logging configuration."""

import logging
import sys
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: str | None = None) -> None:
    """
    Настройка логирования для приложения.

    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Путь к файлу для записи логов (опционально)
    """
    # Формат логов
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Настройка уровня логирования
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Создаём handlers
    handlers = [logging.StreamHandler(sys.stdout)]

    if log_file:
        # Создаём директорию для логов, если её нет
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    # Настройка root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {log_level}")


def get_logger(name: str) -> logging.Logger:
    """
    Получить logger с указанным именем.

    Args:
        name: Имя logger (обычно __name__)

    Returns:
        Настроенный logger
    """
    return logging.getLogger(name)

