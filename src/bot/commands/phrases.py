"""Phrase management commands (add/delete)."""

import shlex
from bot.vk.sender import send_message
from bot.storage.db_store import PhrasesStore


def handle_add(vk, chat_id: int, args_text: str) -> None:
    """
    Handle add phrase command.

    Args:
        vk: VK API session
        chat_id: Chat ID
        args_text: Command arguments
    """
    parts = shlex.split(args_text.strip())

    if len(parts) != 2:
        send_message(vk, chat_id, 'Неправильно! Используй: \\добавить "ключ" "ответ"')
        return

    target, answer = parts
    store = PhrasesStore()
    store.add_phrase(target.lower(), answer)
    send_message(vk, chat_id, f'Добавил "{target}" → "{answer}"')


def handle_delete(vk, chat_id: int, args_text: str) -> None:
    """
    Handle delete phrase command.

    Args:
        vk: VK API session
        chat_id: Chat ID
        args_text: Command arguments
    """
    parts = shlex.split(args_text.strip())

    if len(parts) != 1:
        send_message(vk, chat_id, 'Неправильно! Используй: \\удалить "ключ"')
        return

    delete_phrase = parts[0].lower()
    store = PhrasesStore()
    
    if store.delete_phrase(delete_phrase):
        send_message(vk, chat_id, f'Больше на "{delete_phrase}" не триггерюсь')
    else:
        send_message(vk, chat_id, 'Не нашел у себя этой фразы -_-')


def handle_delete_all(vk, chat_id: int, args_text: str) -> None:
    """
    Handle delete all phrases command.

    Args:
        vk: VK API session
        chat_id: Chat ID
        args_text: Command arguments (should be empty)
    """
    store = PhrasesStore()
    count = store.delete_all_phrases()
    send_message(vk, chat_id, f'Удалил все фразы ({count} шт.) и ответы на них')
