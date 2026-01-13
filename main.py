import vk_api 
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType 
from dotenv import load_dotenv
import os
from transport.vk_longpoll import longpoll_server

load_dotenv()  # Ищет .env в текущей папке

try:
    vk_session = vk_api.VkApi(token=os.getenv("TOKEN"))
    print('VK SESSION OK')
    longpoll = VkBotLongPoll(vk_session, int(os.getenv("GROUP_ID")))
    print('LONGPOLL OK')
except Exception as e:
    print(f"❌ Ошибка при инициализации LongPoll: {e}")
    exit(1)

longpoll_server(longpoll, vk_session)
