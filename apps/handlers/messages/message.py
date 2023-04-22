from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram.methods.ban_chat_member import BanChatMember
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from apps.middlewares.middlewares import FloodControlMiddleware
from apps.database.models import User
from apps.database import orm

router = Router()
router.message.outer_middleware(FloodControlMiddleware())

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
        await message.reply(text=f'У нас новый участник\n\nПривет @{message.new_chat_members[0].username}\n\nОзнакомтесь с правилами группы в закрепленном комментарии <ссылка>')

