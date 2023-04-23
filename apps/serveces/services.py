async def delete_message(bot, chat_id, msg_id):
    """
    Удаление сообщения о муте/бане пользователя
    """
    await bot.delete_message(chat_id, msg_id)