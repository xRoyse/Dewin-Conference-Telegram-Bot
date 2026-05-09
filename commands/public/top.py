from aiogram import types
from sqlalchemy import text

from database.database import get_top_users

from utils.loader import dew_channel, log_message_thread_id

async def top_command_handler(bot, message: types.Message):
    group_id = message.chat.id
    top_users = await get_top_users(group_id)

    if not top_users:
        await message.answer("Топ пользователей пуст.")
        return

    top_message = "<b>🏆 ТОП пользователей.</b>\n\n"
    for i, user in enumerate(top_users, start=1):
        user_id = user['user_id']  
        username = user['username'] if user['username'] else 'Неизвестен'
        sms_count = user['sms']
        
        top_message += f"<b>{i}. <a href='tg://user?id={user_id}'>{username}</a>, Кол-во сообщений: <code>{sms_count}</code></b>\n"

    await message.answer(top_message, parse_mode="HTML")
    await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/top</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n"
            f"<b>✉️ Полученное сообщение:</b>"
            f"<blockquote>{top_message}</blockquote>",
            parse_mode="HTML", 
            message_thread_id=log_message_thread_id
            )