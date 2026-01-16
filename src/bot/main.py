"""Main entry point for VK Beseda Bot."""

import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from bot.vk.client import VKClient
from bot.handlers.dispatcher import dispatch_event
from bot.scheduler.scheduler import start_scheduler
from bot.config.logging import setup_logging, get_logger
from bot.config.settings import settings

# Настройка логирования
setup_logging()

logger = get_logger(__name__)


def main():
    """Main function to start the bot."""
    try:
        logger.info("Starting VK Beseda Bot...")

        # Инициализация VK клиента
        vk_client = VKClient()

        # Запуск планировщика
        start_scheduler(vk_client.api)

        # Запуск longpoll сервера
        logger.info("Bot started successfully. Listening for events...")
        for event in vk_client.listen():
            dispatch_event(vk_client.api, event)

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

