

from services import msg_parser
from services.command_handlers import Commands
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType 
import services.command_handlers as command_handlers

def longpoll_server(longpoll, vk_session):
    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                text = event.object.message.get('text', '')
                id = event.chat_id
                print("event:", event.type, "text:", text)
                if event.from_chat and text:
                    if msg_parser.is_mention(text):
                        if msg_parser.get_command(text) is not None:
                            command = msg_parser.get_command(text)
                            match command:
                                case Commands.HELP:
                                    command_handlers.help(vk_session, id)
                                case Commands.ADD:
                                    command_handlers.handle_add(vk_session, id, msg_parser.get_args_from_command(text))
                                case Commands.DELETE:
                                    command_handlers.handle_delete(vk_session, id, msg_parser.get_args_from_command(text))
                        else:
                            command_handlers.handle_okey_alesha(vk_session, id, text)
                    else:
                        command_handlers.handle_trigger_phrase(vk_session, id, text)
                elif event.from_user:
                    pass     
        except Exception as e:
            print(f"Ошибка команды: {e}")
