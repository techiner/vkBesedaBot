"""Message handler for processing incoming messages."""

from bot.vk.utils import is_mention, delete_mention_text
from bot.utils.text import get_command, get_args_from_command
from bot.commands.base import Commands
from bot.commands import help, subscribe, prompt, analyze
from bot.services.phrases_service import find_phrase
from bot.services.ai_service import ask_ai
from bot.config.settings import settings
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
        message = event.object.message
        text = message.get('text', '')
        chat_id = event.chat_id
        peer_id = message.get('peer_id')

        if not event.from_chat or not text:
            return

        # Если это ответ на сообщение бота — передаём связку "ответ + оригинал" в AI
        reply = message.get('reply_message')
        if reply:
            reply_from_id = reply.get('from_id')
            # Сообщения бота в беседе обычно имеют from_id = -GROUP_ID
            if reply_from_id and abs(reply_from_id) == settings.GROUP_ID:
                bot_text = reply.get('text', '')
                combined_prompt = (
                    "Пользователь отвечает на предыдущее сообщение бота.\n\n"
                    f"Сообщение пользователя:\n{text}\n\n"
                    f"Сообщение бота:\n{bot_text}"
                )
                answer = ask_ai(combined_prompt)
                send_message(vk, chat_id, answer)
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
            # _handle_trigger_phrase(vk, chat_id, text)
            pass

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
        case Commands.SUBSCRIBE:
            subscribe.handle_subscribe(vk, chat_id, peer_id, args)
        case Commands.PROMPT:
            prompt.handle_prompt(vk, chat_id, args)
        case Commands.ANALYZE:
            analyze.handle_analyze(vk, chat_id, peer_id, args)
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

