import vk_api 
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType 
import shlex
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Ищет .env в текущей папке
TOKEN = os.getenv("TOKEN")

# from config import TOKEN

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, 235215404)

def sender(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})

def load_phrases():
    filename = "phrases.json"
    # Если файла нет, создаём его с пустой JSON-структурой
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл есть, но пустой или битый — перезаписываем
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}

def find_phrase(text, phrase_database):
    """Поиск фразы без учета регистра"""
    res = []
    for key, value in phrase_database.items():
        if key.lower() in text.lower():
            res.append(value)
    if len(res) > 0:
        return " ".join(res)
    return None

print('START')
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.object.message['text']
        id = event.chat_id
        print("event:", event.type, "text:", text)
        
        if event.from_chat:
            if text and text[0] == '\\':
                if text.startswith('\\alias'):
                    try:
                        parts = shlex.split(text)
                        if len(parts) >= 3:
                            target = parts[1]
                            answer = parts[2]
                            phrase_database = load_phrases()
                            phrase_database[target] = answer
                            with open("phrases.json", "w", encoding="utf-8") as f:
                                json.dump(phrase_database, f, ensure_ascii=False, indent=2)
                    except Exception as e:
                        print(f"Ошибка команды: {e}")
            else:
                phrase_database = load_phrases()
                answer = find_phrase(text, phrase_database)
                if answer:
                    sender(id, answer)
        elif event.from_user:
            pass