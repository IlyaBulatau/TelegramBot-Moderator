from aiogram import Bot
from aiogram import BaseMiddleware, types
from aiogram.types.chat_permissions import ChatPermissions
from aiogram.methods.restrict_chat_member import RestrictChatMember
from aiogram.types.chat_member_administrator import ChatMemberAdministrator

from datetime import timedelta
import redis as r
import asyncio

from apps.config.constant import THROTTLING_MSG, THROTTLING_SEC
from apps.database import orm
from apps.database.models import User

redis = r.Redis(decode_responses='utf-8', encoding='utf-8')

class FloodControlMiddleware(BaseMiddleware):
    """
    Анти-флуд система если юзер в групповом чате либо канале отправляет больше THROTTLING_MSG сообщений в THROTTLING_SEC секунды его мутят
    Не распостраняется на администраторов группы
    """

    async def __call__(self, handler, event: types.Message, data):
        #проверка на приватный чат
        if event.chat.type == 'privat':
            return await handler(event, data)
                        
        #проверка на админа
        # statuses = ('creator', 'administrator')
        # user = await Bot.get_chat_member(data['bot'], event.chat.id, event.from_user.id) 
        # if user.status in statuses:
        #     return await handler(event, data)

        #если юзера нету в кэшэ то начинаем отслеживать
        user_id = event.from_user.id
        if not (str(user_id) in redis.keys()):
            redis.set(user_id, 0, ex=THROTTLING_SEC)

        # каждое сообщение прибавляем +1
        redis.set(user_id, int(redis[user_id])+1, ex=THROTTLING_SEC)
        #если количество сообщений больше THROTTLING_MSG в течении THROTTLING_SEC секунд  то мутим его
        if int(redis.get(user_id)) > THROTTLING_MSG:
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
                msg = await data['bot'].send_message(chat_id=event.chat.id, text=f'Вы слишком часто пишите в чат @{event.from_user.username}\n\nНаложено ограничения отправки сообщений на 2 минуты')
                await RestrictChatMember(
                    chat_id=event.chat.id, 
                    user_id=event.from_user.id, 
                    permissions=permissions, 
                    until_date=timedelta(minutes=2),
                    )
                await asyncio.sleep(20)
                await data['bot'].delete_message(event.chat.id, msg.message_id)
            elif warning == 1:
                orm.update_user_warning(event.from_user.id, User)
                msg2 = await data['bot'].send_message(chat_id=event.chat.id, text=f'Вы слишком часто пишите в чат @{event.from_user.username}\n\nНа этот раз наложено ограничения отправки сообщений на 30 минут')
                await RestrictChatMember(
                    chat_id=event.chat.id, 
                    user_id=event.from_user.id, 
                    permissions=permissions, 
                    until_date=timedelta(minutes=30),
                    )
                await asyncio.sleep(20)
                await data['bot'].delete_message(event.chat.id, msg2.message_id)
            else:
                msg3 = await data['bot'].send_message(event.chat.id,f'Пользователь @{event.from_user.username} удален из чата за флуд')
                await Bot.ban_chat_member(data['bot'], event.chat.id, event.from_user.id)
                await asyncio.sleep(20)
                await data['bot'].delete_message(event.chat.id, msg3.message_id)

            

        return await handler(event, data)
    

# Кэш с с помощью библиотеки cachetools
    #from cachetools import TTLCache
        # cache = {'throttling': TTLCache(maxsize=10.0, ttl=THROTTLING_SEC)}
        # if not (user_id in self.cache['throttling']):
        #     self.cache['throttling'][user_id] = 0
        # self.cache['throttling'][user_id] += 1
        # if self.cache['throttling'][user_id] > THROTTLING_MSG:
