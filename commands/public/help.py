from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.loader import dew_channel, log_message_thread_id

async def help_command_hendler(bot, message: types.Message):
    help_text = (
        "<b>Популярные команды:</b>\n\n"
        "<b>/sms (текст)</b> - Уведомление участников группы в ЛС\n"
        "<b>/all</b> - Упоминание всех пользователей в группе\n"
        "<b>/top</b> - Топ пользователей по количеству сообщений\n"
    )
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔗 Список всех команд бота", url="https://dewinbot.ru/commands"))
    
    await message.reply(help_text, reply_markup=keyboard, parse_mode="HTML")
    await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/help</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
            parse_mode="HTML", 
            message_thread_id=log_message_thread_id
            )