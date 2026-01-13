import vk_api 
from vk_api.bot_longpoll import VkBotLongPoll
from dotenv import load_dotenv

load_dotenv()  # Ищет .env в текущей папке
TOKEN = "vk1.a.nbQQI73t4T9Vqj5HPg3SE5L_LBfrRgxMtNUKVlZu5BsgIid9WADnutsW04OsnvsLnFjq-9cAxSNODA-_n0BDktxZ6aYuOohDqExaG2o8eW7dgdWRpdt_6C-Mm7CMUulQEHYWPjApzCtnt8QvC_Idslkwpapsa2epglXT08VZsimYlWEFykMVhuDOBd_-rZgjR5puCxMGmxiCnr6qf660xg"
GROUP_ID = 235262298
PHRASES_FILENAME = 'phrases.json'

try:
    vk_session = vk_api.VkApi(token=TOKEN)
    print('VK SESSION OK')
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    print('LONGPOLL OK')
except Exception as e:
    print(f"❌ Ошибка при инициализации LongPoll: {e}")
    exit(1)
