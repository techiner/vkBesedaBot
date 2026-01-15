import os
# from gigachat import GigaChat
# from gigachat.models import Chat, Messages, MessagesRole
from openai import OpenAI


# Глобальный клиент (создаётся один раз)
client = OpenAI(
    base_url="https://neuroapi.host/v1",
    api_key=os.getenv("NEUROAPI_API_KEY"),
)


def ask(ai_prompt):
    completion = client.chat.completions.create(
        model="gpt-5-mini",  # Проверь, что модель существует
        messages=[{"role": "user", "content": ai_prompt}],  # Используй параметр!
    )
    return completion.choices[0].message.content

def get_quote():
    completion = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": "Напиши одну цитату о жизни и подпиши ее автора"}], 
    )
    return completion.choices[0].message.content


