from aiogram import Router, Bot
from aiogram.types import Message, LabeledPrice, successful_payment
from aiogram.filters import Command
from aiogram.types.pre_checkout_query import PreCheckoutQuery

from datetime import timedelta, datetime

from apps.middlewares import middlewares
from apps.database.models import User
from apps.database import orm
from apps.serveces import services
from apps.config.config import PAYMENTS

router = Router()
router.message.outer_middleware(middlewares.FloodControlMiddleware())
router.message.outer_middleware(middlewares.SwearWorldControlMiddleware())
router.message.outer_middleware(middlewares.EntitiesControlMiddleware())


@router.message(Command(commands='upstatus'))
async def update_process(message: Message, bot: Bot):
    if message.chat.type != 'private':
        return
    else:
        price = LabeledPrice(label='Оплата за админку', amount=1*10000)
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Платеж',
            description='Получение админки',
            payload='Admin',
            provider_token=PAYMENTS,
            currency='USD',
            prices=[price],
            max_tip_amount=1000000,
            start_parameter='Picachy2001Bot',
            provider_data=None,
            need_name=True,
            need_email=True,
            need_phone_number=True,
            need_shipping_address=False,
            send_email_to_provider=False,
            send_phone_number_to_provider=False,
            is_flexible=False,
            protect_content=True,
            disable_notification=False,
            )

@router.pre_checkout_query()
async def pre_checkout_query_process(pcq: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pcq.id, ok=True)

@router.message(successful_payment.SuccessfulPayment)
async def successful_payment_process(message: Message, bot: Bot):
    currency = message.successful_payment.currency
    total_amount = message.successful_payment.total_amount
    id_payment = message.successful_payment.telegram_payment_charge_id
    await bot.send_message(chat_id=message.chat.id, 
                        text=f'Оплата на сумму {total_amount} {currency} прошла успешно,\n\nПоздрвляем вы теперь админ группы!\n\nКод оплаты - {id_payment}')


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
        middlewares.sched.add_job(func=services.delete_message, trigger='date', run_date=datetime.now()+timedelta(seconds=20), args=[bot, message.chat.id, msg.message_id])
    middlewares.sched.add_job(func=services.delete_message, trigger='date', run_date=datetime.now()+timedelta(seconds=20), args=[bot, message.chat.id, message.message_id])
    
    

@router.message(lambda msg: msg.left_chat_member)
async def leave_user(message: Message):
    """
    Выход участника из группы
    """
    await message.delete()
    
