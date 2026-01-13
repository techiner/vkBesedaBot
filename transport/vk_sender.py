

def sender(vk, id, text) -> None:
    try:
        vk.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
