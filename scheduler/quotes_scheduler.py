import time
import schedule

from infra import subscription_store_service
from services.ai_service import get_quote
from transport.vk_sender import sender

def job_quote(vk):
    subscribers = subscription_store_service.load_subscriptions()
    print(f"Цитаты для отправки ({len(subscribers)} подписчиков):")

    for peer_id in subscribers:
        # Для бесед chat_id = peer_id - 2000000000
        chat_id = peer_id - 2000000000
        sender(
            vk, 
            chat_id, 
            "[🤭 Шутка-минутка]"
        )
    sender(vk, get_quote(vk))

def scheduler_qoute_loop(vk):
    schedule.every().day.at("20:00").do(lambda: job_quote(vk))
    while True:
        schedule.run_pending()
        time.sleep(1)