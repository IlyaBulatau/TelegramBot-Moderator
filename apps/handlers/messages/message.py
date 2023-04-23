from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from datetime import timedelta, datetime

from apps.middlewares.middlewares import FloodControlMiddleware, SwearWorldControlMiddleware, sched
from apps.database.models import User
from apps.database import orm
from apps.serveces import services

router = Router()
router.message.outer_middleware(FloodControlMiddleware())
router.message.outer_middleware(SwearWorldControlMiddleware())

class BanStateUser(StatesGroup):
    user_id = State()

@router.message(lambda msg: msg.new_chat_members)
async def join_user(message: Message, bot: Bot):
    """
    отслеживает добавление участника в группу
    """
    user_id = message.new_chat_members[0].id
    if orm.is_user_in_db(user_id, User):
        return
    else:
        orm.add_user_to_db(user_id, User)
        msg = await message.reply(text=f'У нас новый участник\n\nПривет @{message.new_chat_members[0].username}\n\nОзнакомтесь с правилами группы в закрепленном сообщении')
        sched.add_job(func=services.delete_message, trigger='date', run_date=datetime.now()+timedelta(seconds=20), args=[bot, message.chat.id, msg.message_id])
    sched.add_job(func=services.delete_message, trigger='date', run_date=datetime.now()+timedelta(seconds=20), args=[bot, message.chat.id, message.message_id])
    

@router.message(lambda msg: msg.left_chat_member)
async def leave_user(message: Message):
    """
    Выход участника из группы
    """
    await message.delete()




