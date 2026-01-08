import vk_api 
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType 
import shlex
import json
from enum import Enum
from dotenv import load_dotenv
import os
import re

load_dotenv()  # Ищет .env в текущей папке
TOKEN = os.getenv("TOKEN")
PHRASES_FILENAME = 'phrases.json'

# from config import TOKEN

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, 235215404)

def sender(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})

def load_phrases(filename):
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
    
def save_phrases(filename, json_data):
    """
    Сохраняет текст в файл. Если файл существует — дописывает в конец.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка записи в {filename}: {e}")

def find_phrase(text, phrase_database):
    """Поиск фразы без учета регистра"""
    res = []
    for key, value in phrase_database.items():
        pattern = r'(?<!\w)' + re.escape(key) + r'(?!\w)'
        if re.search(pattern, text, flags=re.IGNORECASE):
            res.append(value)

    if len(res) > 0:
        return " ".join(res)
    return None

class Commands(str, Enum):
    HELP = '\\help'
    ADD = '\\добавить'
    DELETE = '\\удалить'

help_list = {
    Commands.HELP.value: f'{Commands.HELP.value}',
    Commands.ADD.value: f'{Commands.ADD.value} "ищу" "отвечаю"',
    Commands.DELETE.value: f'{Commands.DELETE.value} "эту фразу я искать больше не стану"'
}

print('START')
for event in longpoll.listen():
    try:
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.object.message.get('text', '')
            id = event.chat_id
            print("event:", event.type, "text:", text)
            
            if event.from_chat and text:
                if text[0] == '\\':
                    if text.startswith(Commands.HELP):
                        help_answer = ''
                        for key, value in help_list.items():
                            help_answer += f'{value}\n'
                        sender(id, help_answer)
                    if text.startswith(Commands.ADD):
                            parts = shlex.split(text)
                            if len(parts) == 3:
                                target = parts[1]
                                answer = parts[2]
                                phrase_database = load_phrases(PHRASES_FILENAME)
                                phrase_database[target] = answer
                                save_phrases(PHRASES_FILENAME, phrase_database)
                                sender(id, f'Добавил "{target}" "{answer}"')
                    if text.startswith(Commands.DELETE):
                        parts = shlex.split(text)
                        if len(parts) == 2:
                            delete_phrase = parts[1]
                            phrase_database = load_phrases(PHRASES_FILENAME)
                            if (delete_phrase not in phrase_database):
                                sender(id, 'Не нашел у себя этой фразы -_-')
                            else: 
                                del phrase_database[delete_phrase]
                                save_phrases(PHRASES_FILENAME, phrase_database)
                                sender(id, f'Больше на "{delete_phrase}" не триггерюсь')
                else:
                    phrase_database = load_phrases(PHRASES_FILENAME)
                    answer = find_phrase(text, phrase_database)
                    if answer:
                        sender(id, answer)
            elif event.from_user:
                pass     
    except Exception as e:
        print(f"Ошибка команды: {e}")