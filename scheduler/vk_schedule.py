import threading
from scheduler.jokes_scheduler import scheduler_jokes_loop
from scheduler.quotes_scheduler import scheduler_qoute_loop

def start_scheduler(vk):
    threading.Thread(target=scheduler_jokes_loop, args=(vk,), daemon=True).start()
    threading.Thread(target=scheduler_qoute_loop, args=(vk,), daemon=True).start()
    print("Планировщик заданий запущен")