from aiogram import Bot
from aiogram.types.bot_command import BotCommand

async def menu_commands(bot: Bot):

    commands = [
        BotCommand(
        command='help',
        description='Справка'
        ),
        BotCommand(
        command='contact',
        description='Написать разработчику'
        ),
        BotCommand(
        command='rules',
        description='Правила чата'
        )
    ]

    await bot.set_my_commands(commands)