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
    user_id = message.from_user.id
    orm.add_user_to_db(user_id, User)
    await message.reply(text=f'У нас новый участник\n\nПривет {message.from_user.first_name}')

# @router.message()
# async def other_msg(message: Message):
#     if not orm.is_user_in_db(message.from_user.id, User):
#         orm.add_user_to_db(message.from_user.id, User)
#     await message.answer(text='Вы отправили сообщение')
    
# @router.message(Command(commands='ban'))
# async def ban_user(message: Message, state: FSMContext):
#     await state.set_state(BanStateUser.user_id)
#     await message.answer(text='Укажите пользователя переслав его сообщения')

# @router.message(BanStateUser.user_id, lambda msg:msg.forward_from )
# async def process_ban_user(message: Message, state: FSMContext):
#     await state.clear()
#     user_id = message.forward_from.id
#     await BanChatMember(chat_id=message.chat.id, user_id=user_id, until_date=31000)
#     print(f'Заблокирован {message.forward_from.first_name}')

# @router.message(BanStateUser.user_id)
# async def procee_not_ban(message: Message):
#     await message.answer(text="Перешлите собщение")
    