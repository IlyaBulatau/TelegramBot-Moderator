from aiogram import Bot
from aiogram import BaseMiddleware, types
from aiogram.types.chat_permissions import ChatPermissions
from aiogram.methods.restrict_chat_member import RestrictChatMember
from aiogram.types.chat_member_administrator import ChatMemberAdministrator

from datetime import timedelta
from cachetools import TTLCache

from apps.config.constant import THROTTLING_MSG, THROTTLING_SEC
from apps.database import orm
from apps.database.models import User

class FloodControlMiddleware(BaseMiddleware):
    """
    Анти-флуд система если юзер в групповом чате либо канале отправляет больше THROTTLING_MSG сообщений в THROTTLING_SEC секунды его мутят
    Не распостраняется на администраторов группы
    """
    cache = {'throttling': TTLCache(maxsize=10.0, ttl=THROTTLING_SEC)}

    async def __call__(self, handler, event: types.Message, data):
        #проверка на приватный чат
        if event.chat.type == 'privat':
            return await handler(event, data)

        #проверка на админа
        statuses = ('creator', 'administrator')
        user = await Bot.get_chat_member(data['bot'], event.chat.id, event.from_user.id) 
        if user.status in statuses:
            return await handler(event, data)

        #если юзера нету в кэшэ то начинаем отслеживать
        user_id = event.from_user.id
        if not (user_id in self.cache['throttling']):
            self.cache['throttling'][user_id] = 0

        self.cache['throttling'][user_id] += 1

        #если количество сообщений больше THROTTLING_MSG в THROTTLING_SEC секунд  то мутим его
        if self.cache['throttling'][user_id] > THROTTLING_MSG:
            warning = orm.get_user_warnings_db(event.from_user.id, User)
            permissions= {
                "can_send_messages":False,
                "can_send_documents":False,
                "can_send_audios":False,
                "can_send_other_messages":False,
                "can_send_photos":False,
                "can_send_video_notes":False,
                "can_send_polls":False,
                "can_send_videos":False,
                "can_send_voice_notes":False,
                }          
                 
            await event.delete()

            if warning == 0:
                orm.update_user_warning(event.from_user.id, User)
                await data['bot'].send_message(chat_id=event.chat.id, text='Вы слишком часто пишите в чат\n\nНаложено ограничения отправки сообщений на 2 минуты')
                await RestrictChatMember(chat_id=event.chat.id, user_id=event.from_user.id, permissions=permissions, until_date=timedelta(minutes=2))
            elif warning == 1:
                orm.update_user_warning(event.from_user.id, User)
                await data['bot'].send_message(chat_id=event.chat.id, text='Вы слишком часто пишите в чат\n\nНа этот раз наложено ограничения отправки сообщений на 30 минут')
                await RestrictChatMember(chat_id=event.chat.id, user_id=event.from_user.id, permissions=permissions, until_date=timedelta(minutes=30))
            else:
                await Bot.ban_chat_member(data['bot'], event.chat.id, event.from_user.id)

            

        return await handler(event, data)
    
