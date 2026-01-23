"""VK history messages service."""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from bot.config.logging import get_logger

logger = get_logger(__name__)

# Типы вложений для маркировки
ATTACHMENT_TYPES = {
    'photo': '[photo]',
    'video': '[video]',
    'audio': '[audio]',
    'doc': '[document]',
    'link': '[link]',
    'wall': '[wall_post]',
    'wall_reply': '[wall_reply]',
    'sticker': '[sticker]',
    'gift': '[gift]',
    'graffiti': '[graffiti]',
    'audio_message': '[voice]',
    'poll': '[poll]',
    'market': '[market]',
}


def get_messages_history(vk, peer_id: int, days: int = 7) -> List[Dict[str, Any]]:
    """
    Получить историю сообщений за указанное количество дней.

    Args:
        vk: VK API session
        peer_id: Peer ID чата
        days: Количество дней для получения истории

    Returns:
        Список сообщений в хронологическом порядке
    """
    messages = []
    offset = 0
    count = 200  # Максимум за один запрос
    
    # Вычисляем timestamp для начала периода
    start_date = datetime.now() - timedelta(days=days)
    start_ts = int(start_date.timestamp())
    
    logger.info(f"Fetching messages from {start_date.date()} (last {days} days) for peer_id={peer_id}")

    try:
        while True:
            # Получаем сообщения постранично
            response = vk.method('messages.getHistory', {
                'peer_id': peer_id,
                'offset': offset,
                'count': count,
                'rev': 0  # 0 = от новых к старым
            })
            
            items = response.get('items', [])
            if not items:
                break
            
            # Фильтруем по дате и собираем сообщения
            for item in items:
                msg_date = datetime.fromtimestamp(item['date'])
                
                # Если сообщение старше нужного периода, прекращаем сбор
                if msg_date < start_date:
                    return sorted(messages, key=lambda x: x['date'])
                
                messages.append(item)
            
            # Если получили меньше, чем запрашивали - последняя страница
            if len(items) < count:
                break
            
            offset += count
            
            # Защита от бесконечного цикла
            if offset > 10000:  # Максимум 10k сообщений
                logger.warning("Reached maximum offset limit")
                break
        
        # Сортируем по дате (хронологически)
        return sorted(messages, key=lambda x: x['date'])
        
    except Exception as e:
        logger.error(f"Error fetching messages history: {e}")
        raise


def format_message_attachments(message: Dict[str, Any]) -> str:
    """
    Форматирует вложения сообщения в маркеры.

    Args:
        message: Объект сообщения из VK API

    Returns:
        Строка с маркерами вложений
    """
    attachments = message.get('attachments', [])
    if not attachments:
        return ''
    
    markers = []
    for attachment in attachments:
        attach_type = attachment.get('type', '')
        marker = ATTACHMENT_TYPES.get(attach_type, f'[{attach_type}]')
        markers.append(marker)
    
    return ' ' + ' '.join(markers) if markers else ''


def get_user_name(vk, user_id: int) -> str:
    """
    Получить имя пользователя по ID.

    Args:
        vk: VK API session
        user_id: ID пользователя

    Returns:
        Строка "Имя Фамилия" или "Пользователь {id}" в случае ошибки
    """
    try:
        # Для пользователей (положительный ID)
        if user_id > 0:
            users = vk.method('users.get', {
                'user_ids': user_id,
                'fields': 'first_name,last_name'
            })
            if users:
                user = users[0]
                return f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        
        # Для групп (отрицательный ID) - можно получить информацию о группе
        # Но обычно сообщения от ботов в беседах имеют положительные ID
        return f"Пользователь {user_id}"
        
    except Exception as e:
        logger.warning(f"Error getting user name for {user_id}: {e}")
        return f"Пользователь {user_id}"


def format_messages_for_analysis(vk, messages: List[Dict[str, Any]]) -> str:
    """
    Форматирует сообщения для отправки в AI.

    Args:
        vk: VK API session
        messages: Список сообщений

    Returns:
        Отформатированный текст сообщений
    """
    if not messages:
        return ""
    
    formatted_lines = []
    
    for msg in messages:
        from_id = msg.get('from_id', 0)
        text = msg.get('text', '').strip()
        date = datetime.fromtimestamp(msg['date'])
        
        # Пропускаем сообщения от бота (обычно from_id совпадает с GROUP_ID)
        # Можно добавить проверку, но пока оставим все
        
        # Получаем имя пользователя
        user_name = get_user_name(vk, from_id)
        
        # Форматируем вложения
        attachments = format_message_attachments(msg)
        
        # Формируем строку
        if text or attachments:
            formatted_line = f"{user_name}: {text}{attachments}"
            formatted_lines.append(formatted_line)
    
    return '\n'.join(formatted_lines)

