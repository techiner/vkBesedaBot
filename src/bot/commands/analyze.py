"""Analyze command handler for weekly chat analysis."""

import time
from typing import List
from bot.vk.sender import send_message
from bot.vk.history import get_messages_history, format_messages_for_analysis
from bot.services.ai_service import ask_ai_analysis
from bot.config.logging import get_logger

logger = get_logger(__name__)

# Максимальная длина сообщения VK (4096 символов)
MAX_MESSAGE_LENGTH = 4000  # Оставляем запас


def split_long_message(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> List[str]:
    """
    Разбивает длинный текст на части.

    Args:
        text: Текст для разбиения
        max_length: Максимальная длина одной части

    Returns:
        Список частей текста
    """
    if len(text) <= max_length:
        return [text]
    
    parts = []
    lines = text.split('\n')
    current_part = []
    current_length = 0
    
    for line in lines:
        line_length = len(line) + 1  # +1 для переноса строки
        
        if current_length + line_length > max_length:
            if current_part:
                parts.append('\n'.join(current_part))
                current_part = []
                current_length = 0
        
        current_part.append(line)
        current_length += line_length
    
    if current_part:
        parts.append('\n'.join(current_part))
    
    return parts


def handle_analyze(vk, chat_id: int, peer_id: int, args_text: str) -> None:
    """
    Handle analyze command - анализирует беседу за неделю.

    Args:
        vk: VK API session
        chat_id: Chat ID
        peer_id: Peer ID
        args_text: Command arguments (не используется, но может быть "за неделю")
    """
    try:
        # Отправляем уведомление о начале анализа
        send_message(vk, chat_id, "📊 Начинаю анализ беседы за последние 7 дней...")
        
        # Получаем историю сообщений
        try:
            messages = get_messages_history(vk, peer_id, days=7)
        except Exception as e:
            logger.error(f"Error fetching messages history: {e}")
            send_message(vk, chat_id, "❌ Ошибка при получении истории сообщений. Проверь права бота.")
            return
        
        if not messages:
            send_message(vk, chat_id, "📭 За последние 7 дней в беседе нет сообщений для анализа.")
            return
        
        # Форматируем сообщения
        try:
            formatted_messages = format_messages_for_analysis(vk, messages)
        except Exception as e:
            logger.error(f"Error formatting messages: {e}")
            send_message(vk, chat_id, "❌ Ошибка при форматировании сообщений.")
            return
        
        if not formatted_messages.strip():
            send_message(vk, chat_id, "📭 Не удалось получить текстовые сообщения для анализа.")
            return
        
        # Отправляем в AI для анализа
        analysis_prompt = f"""Проанализируй переписку из беседы за последнюю неделю и создай краткую сводку:

{formatted_messages}

Сделай анализ по следующим пунктам:
1. Кратко о чем говорили (2-3 предложения)
2. Основные темы недели (список 3-5 тем)
3. Принятые решения (если были)
4. Открытые вопросы (если остались)
5. Общий тон беседы (формальный/неформальный, позитивный/негативный и т.д.)

Ответ должен быть структурированным и читаемым. Используй эмодзи для наглядности."""
        
        logger.info(f"Sending {len(messages)} messages to AI for analysis")
        
        try:
            analysis_result = ask_ai_analysis(analysis_prompt)
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            send_message(vk, chat_id, "❌ Ошибка при анализе через AI. Попробуй позже.")
            return
        
        if not analysis_result or analysis_result == "Извини, произошла ошибка при обработке запроса.":
            send_message(vk, chat_id, "❌ Не удалось получить анализ от AI.")
            return
        
        # Разбиваем длинный результат на части и отправляем
        parts = split_long_message(analysis_result)
        
        for i, part in enumerate(parts):
            if i == 0:
                send_message(vk, chat_id, f"📊 Анализ беседы за последние 7 дней:\n\n{part}")
            else:
                send_message(vk, chat_id, part)
            
            # Небольшая задержка между сообщениями, чтобы не флудить
            if i < len(parts) - 1:
                time.sleep(0.5)
        
        logger.info(f"Analysis completed successfully for chat {chat_id}")
        
    except Exception as e:
        logger.error(f"Unexpected error in analyze command: {e}", exc_info=True)
        send_message(vk, chat_id, "❌ Произошла неожиданная ошибка при анализе.")

