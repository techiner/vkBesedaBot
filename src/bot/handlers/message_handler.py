"""Message handler for processing incoming messages."""

from bot.vk.utils import is_mention, delete_mention_text
from bot.utils.text import get_command, get_args_from_command
from bot.commands.base import Commands
from bot.commands import help, phrases, subscribe, prompt
from bot.services.phrases_service import find_phrase
from bot.vk.sender import send_message
from bot.handlers.errors import handle_error


def handle_message(vk, event) -> None:
    """
    Handle incoming message event.

    Args:
        vk: VK API session
        event: VK bot event
    """
    try:
        text = event.object.message.get('text', '')
        chat_id = event.chat_id
        peer_id = event.object.message.get('peer_id')

        if not event.from_chat or not text:
            return

        # Проверяем упоминание бота
        if is_mention(text):
            # Удаляем упоминание для дальнейшей обработки
            text_without_mention = delete_mention_text(text)
            command = get_command(text_without_mention)

            if command:
                args = get_args_from_command(text_without_mention)
                _handle_command(vk, chat_id, peer_id, command, args)
            else:
                # Если команды нет, но есть упоминание - обрабатываем как AI запрос
                prompt.handle_prompt(vk, chat_id, text_without_mention)
        else:
            # Обрабатываем как триггерную фразу
            _handle_trigger_phrase(vk, chat_id, text)

    except Exception as e:
        handle_error(e, "при обработке сообщения")


def _handle_command(vk, chat_id: int, peer_id: int, command: Commands, args: str) -> None:
    """
    Route command to appropriate handler.

    Args:
        vk: VK API session
        chat_id: Chat ID
        peer_id: Peer ID
        command: Command enum
        args: Command arguments
    """
    match command:
        case Commands.HELP:
            help.handle_help(vk, chat_id)
        case Commands.ADD:
            phrases.handle_add(vk, chat_id, args)
        case Commands.DELETE:
            phrases.handle_delete(vk, chat_id, args)
        case Commands.SUBSCRIBE:
            subscribe.handle_subscribe(vk, chat_id, peer_id, args)
        case Commands.PROMPT:
            prompt.handle_prompt(vk, chat_id, args)
        case _:
            pass


def _handle_trigger_phrase(vk, chat_id: int, phrase_text: str) -> None:
    """
    Handle trigger phrase matching.

    Args:
        vk: VK API session
        chat_id: Chat ID
        phrase_text: Text to check for triggers
    """
    answer = find_phrase(phrase_text.lower())
    if answer:
        send_message(vk, chat_id, answer)

