
import shlex
from domain.commands import Commands
from services import ai_service, phrases_service
import infra.phrases_store_service as phrases_store_service
import infra.subscription_store_service as subscription_store_service
from transport import vk_sender


def help(vk, chat_id):
    help_list = {
        Commands.HELP.value: f'{Commands.HELP.value}',
        Commands.ADD.value: f'{Commands.ADD.value} "ищу" "отвечаю"',
        Commands.DELETE.value: f'{Commands.DELETE.value} "эту фразу я искать больше не стану"',
        Commands.PROMPT.value: f'набирай вопрос и я отвечу',
        Commands.SUBSCRIBE.value: f'{Commands.SUBSCRIBE.value} "шутки" — подписаться на ежедневные шутки',
    }

    help_answer = ''
    for key, value in help_list.items():
        help_answer += f'{value}\n'
    vk_sender.sender(vk, chat_id, help_answer.strip())


def handle_add(vk, chat_id, args_text: str) -> None:
    """Обрабатывает команду \добавить ..."""
    parts = shlex.split(args_text.strip())
    
    if len(parts) != 2:
        vk_sender.sender(vk, chat_id, 'Неправильно! Используй: \\добавить "ключ" "ответ"')
        return
    
    target, answer = parts
    phrase_database = phrases_store_service.load_phrases()
    phrase_database[target.lower()] = answer
    phrases_store_service.save_phrases(phrase_database)
    vk_sender.sender(vk, chat_id, f'Добавил "{target}" → "{answer}"')


def handle_delete(vk, chat_id, args_text: str) -> None:
    parts = shlex.split(args_text.strip())
    
    if len(parts) != 1:
        vk_sender.sender(vk, chat_id, 'Неправильно! Используй: \\удалить "ключ"')
        return
    
    delete_phrase = parts[0].lower()
    phrase_database = phrases_store_service.load_phrases()
    
    if delete_phrase not in phrase_database:
        vk_sender.sender(vk, chat_id, 'Не нашел у себя этой фразы -_-')
    else:
        del phrase_database[delete_phrase]
        phrases_store_service.save_phrases(phrase_database)
        vk_sender.sender(vk, chat_id, f'Больше на "{delete_phrase}" не триггерюсь')


def handle_trigger_phrase(vk, chat_id, phrase_text) -> None:
    answer = phrases_service.find_phrase(phrase_text.lower())
    if answer:
        vk_sender.sender(vk, chat_id, answer)


def handle_okey_alesha(vk, chat_id, ai_prompt) -> None:
    answer = ai_service.ask(ai_prompt)
    vk_sender.sender(vk, chat_id, answer)


def handle_subscribe(vk, chat_id, peer_id: int, args_text: str) -> None:
    """
    Обрабатывает команду подписки на рассылку шуток:
    @aleshabotan подписаться "шутки"
    """
    parts = shlex.split(args_text.strip())

    if len(parts) != 1 or parts[0].lower() != "шутки":
        vk_sender.sender(
            vk,
            chat_id,
            'Неправильно! Используй: подписаться "шутки"',
        )
        return

    subs = subscription_store_service.load_subscriptions()

    if peer_id in subs:
        vk_sender.sender(vk, chat_id, "Ты уже подписан на мои шутки!")
        return

    subs.append(peer_id)
    subscription_store_service.save_subscriptions(subs)
    vk_sender.sender(vk, chat_id, "Подписал этот чат на ежедневные шутки 🤡")