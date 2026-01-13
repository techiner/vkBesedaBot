

from commands import Commands
import commands
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType 
import shlex

def longpoll_server(longpoll, vk_session):
    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                text = event.object.message.get('text', '')
                id = event.chat_id
                print("event:", event.type, "text:", text)
                
                if event.from_chat and text:
                    if text[0] == '\\':
                        command = shlex.split(text.strip())[0]
                        match command:
                            case Commands.HELP:
                                commands.help(vk_session, id)
                            case Commands.ADD:
                                commands.add(vk_session, id, text[len(Commands.ADD):].strip())
                            case Commands.DELETE:
                                commands.delete(vk_session, id, text[len(Commands.DELETE):].strip())
                            case 'окейалеша':
                                commands.okey_alesha(vk_session, id, text)
                    else:
                        commands.handle_trigger_phrase(vk_session, id, text)
                elif event.from_user:
                    pass     
        except Exception as e:
            print(f"Ошибка команды: {e}")
