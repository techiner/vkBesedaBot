"""AI prompt command handler."""

from bot.vk.sender import send_message
from bot.services.ai_service import ask_ai


def handle_prompt(vk, chat_id: int, prompt_text: str) -> None:
    """
    Handle AI prompt command.

    Args:
        vk: VK API session
        chat_id: Chat ID
        prompt_text: User prompt text
    """
    answer = ask_ai(prompt_text)
    send_message(vk, chat_id, answer)

