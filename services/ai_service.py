import os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

def ask(ai_prompt):
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
    
    return answer