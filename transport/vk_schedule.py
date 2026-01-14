from functools import partial
from itertools import islice
import threading
import time
import schedule
import csv
import random

from transport.vk_sender import sender
import infra.subscription_store_service as subscription_store_service


def job_9am(vk):
    print("Запуск задания в 9:00")
    path = "./data/clean_comedy_gold_ru.csv"
    jokes_count = 2
    jokes_indexes = random.sample(range(1, 1000), jokes_count)  # Выбираем 3 случайных индекса
    jokes_msgs = []

    for row_index in jokes_indexes:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Считываем заголовок
            row = next(islice(reader, row_index-1, row_index), None)  # Считываем нужную строку
            if row:
                jokes_msgs.append(row[0])  # Добавляем текст шутки в список

    subscribers = subscription_store_service.load_subscriptions()
    print(f"Выбранные шутки для отправки ({len(subscribers)} подписчиков):")

    for peer_id in subscribers:
        # Для бесед chat_id = peer_id - 2000000000
        chat_id = peer_id - 2000000000
        sender(
            vk, 
            chat_id, 
            "[🤭 Шутка-минутка]"
        )
        for msg in jokes_msgs:
            sender(vk, chat_id, msg)
            print(f"[{peer_id} -> chat {chat_id}] {msg}")


def scheduler_loop(vk):
    schedule.every().day.at("17:14").do(lambda: job_9am(vk))
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler(vk):
    threading.Thread(target=scheduler_loop, args=(vk,), daemon=True).start()
    print("Планировщик заданий запущен")