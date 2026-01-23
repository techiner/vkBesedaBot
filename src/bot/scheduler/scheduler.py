"""Scheduler for running periodic tasks."""

import threading
import time
import schedule
from bot.scheduler.jobs import job_quote
from bot.config.logging import get_logger

logger = get_logger(__name__)


def scheduler_loop(vk) -> None:
    """
    Main scheduler loop running in background thread.

    Args:
        vk: VK API session
    """
    # Настройка расписания
    schedule.every().day.at("20:00").do(lambda: job_quote(vk))

    logger.info("Scheduler loop started")

    while True:
        schedule.run_pending()
        time.sleep(1)


def start_scheduler(vk) -> None:
    """
    Start scheduler in background thread.

    Args:
        vk: VK API session
    """
    thread = threading.Thread(target=scheduler_loop, args=(vk,), daemon=True)
    thread.start()
    logger.info("Планировщик заданий запущен")

