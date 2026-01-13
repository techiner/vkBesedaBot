
import phrases
import utils
from enum import Enum
import shlex
from phrases import load_phrases, save_phrases
from httpx import Client, HTTPTransport
from groq import Groq
import os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

class Commands(str, Enum):
    HELP = '\\help'
    ADD = '\\добавить'
    DELETE = '\\удалить'

help_list = {
    Commands.HELP.value: f'{Commands.HELP.value}',
    Commands.ADD.value: f'{Commands.ADD.value} "ищу" "отвечаю"',
    Commands.DELETE.value: f'{Commands.DELETE.value} "эту фразу я искать больше не стану"'
}

def help(vk, chat_id):
    help_answer = ''
    for key, value in help_list.items():
        help_answer += f'{value}\n'
    utils.sender(vk, chat_id, help_answer.strip())

def handle_add(vk, chat_id, command_text):
    """Обрабатывает команду \добавить ..."""
    parts = shlex.split(command_text.strip())
    
    if len(parts) != 2:
        utils.sender(vk, chat_id, 'Неправильно! Используй: \\добавить "ключ" "ответ"')
        return
    
    target, answer = parts
    phrase_database = load_phrases()
    phrase_database[target.lower()] = answer
    save_phrases(phrase_database)
    utils.sender(vk, chat_id, f'Добавил "{target}" → "{answer}"')

def handle_delete(vk, chat_id, command_text):
    parts = shlex.split(command_text.strip())
    
    if len(parts) != 2:
        utils.sender(vk, chat_id, 'Неправильно! Используй: \\удалить "ключ"')
        return
    
    delete_phrase = parts[1].lower()
    phrase_database = load_phrases()
    
    if delete_phrase not in phrase_database:
        utils.sender(vk, chat_id, 'Не нашел у себя этой фразы -_-')
    else:
        del phrase_database[delete_phrase]
        save_phrases(phrase_database)
        utils.sender(vk, chat_id, f'Больше на "{delete_phrase}" не триггерюсь')

def handle_trigger_phrase(vk, chat_id, phrase_text):
    phrase_database = load_phrases()
    answer = phrases.find_phrase(phrase_text.lower(), phrase_database)
    if answer:
        utils.sender(vk, chat_id, answer)

def okey_alesha(vk, chat_id, text):
    ai_prompt = text[len('\\окейалеша '):].strip()
    # Инициализация клиента
    giga = GigaChat(
        credentials=os.getenv("GIGACHAT_API_KEY"),  # base64 "client_id:client_secret"
        verify_ssl_certs=False
    )
    
    # Системный промпт и пользовательское сообщение
    system_message = Messages(
        role=MessagesRole.SYSTEM,
        content="Тебя зовут Алёша. Веди себя настолько высокомерно как можешь. Восхваляй себя в каждом втором предложении разными формулировками(это важно)"
    )
    user_message = Messages(role=MessagesRole.USER, content=ai_prompt)
    payload = Chat(messages=[system_message, user_message])
    
    try:
        response = giga.chat(payload)
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Даже я, великолепный Алёша, иногда сталкиваюсь с помехами: {str(e)}"
    
    utils.sender(vk, chat_id, answer)