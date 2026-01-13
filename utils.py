import shlex
from phrases import load_phrases, save_phrases
import requests
import random

def sender(vk, id, text):
    try:
        vk.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")


def get_random_proxy():
    
    """Берёт случайный прокси с ProxyScrape API"""
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all"
        response = requests.get(url)
        proxy_list = response.text.splitlines()
        # Фильтруем пустые строки и выбираем случайный
        proxy_list = [p.strip() for p in proxy_list if p.strip()]
        if proxy_list:
            return random.choice(proxy_list)
        else:
            print("⚠️ ProxyScrape: список пуст")
            return None
    except Exception as e:
        print(f"Ошибка при получении прокси: {e}")
        return None
