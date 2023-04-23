from aiogram import Bot
from aiogram.types.bot_command import BotCommand

async def menu_commands(bot: Bot):

    commands = [
        BotCommand(
        command='upstatus',
        description='Получение админки'
        )
    ]

    await bot.set_my_commands(commands)