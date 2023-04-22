from apps.config import config
from apps.keyboards.menu import menu_commands

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import Redis, RedisStorage
from apps.handlers.messages import message

import asyncio


async def run():
    bot = Bot(token=config.TOKEN)
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)
    
    dp.include_router(message.router)
    dp.startup.register(menu_commands)

    await dp.start_polling(bot, allowed_update=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(run())

    #TODO - сделать проверку на админа
    # при флуде отсылать сообщения с упоминанием участника группы и удалять сообщения через 20 сек
    
    # проверка на мат
    # уведомления в чат по таймеру
    # при добавлении учатсника приветствие и ссылка на закрепленный комментарий
    # возможность оплаты для получения прав администратора группы
