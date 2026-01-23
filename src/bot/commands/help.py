"""Help command handler."""

from bot.commands.base import Commands
from bot.vk.sender import send_message


def handle_help(vk, chat_id: int) -> None:
    """
    Handle help command.

    Args:
        vk: VK API session
        chat_id: Chat ID
    """
    help_list = {
        Commands.HELP.value: f'{Commands.HELP.value}',
        Commands.PROMPT.value: f'набирай вопрос и я отвечу',
        Commands.SUBSCRIBE.value: f'{Commands.SUBSCRIBE.value} "цитаты" — подписаться на ежедневные цитаты',
        Commands.ANALYZE.value: f'{Commands.ANALYZE.value} — анализ беседы за последние 7 дней',
    }

    help_answer = '\n'.join(help_list.values())
    send_message(vk, chat_id, help_answer.strip())

