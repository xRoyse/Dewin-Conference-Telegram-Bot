from aiogram import types
from database.database import get_admin_level, get_banned_users 
from utils.loader import *

async def banlist_handler(bot, message: types.Message):
    group_id = message.chat.id
    banned_users = await get_banned_users(group_id)
    initiator_level = await get_admin_level(message.from_user.id, group_id)
    
    if initiator_level < 1:
        await message.reply("<b>⛔ У вас недостаточно прав для использования этой команды.</b>", parse_mode="HTML")
        return

    if not banned_users:
        await message.answer("<b>В вашей группе нет забаненых людей, это круто! 😊</b>", parse_mode='html')
        await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/banlist</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n"
            f"<b>✉️ Полученное сообщение:</b>"
            f"<blockquote><b>В вашей группе нет забаненых людей, это круто! 😊</b></blockquote>",
            parse_mode="HTML", message_thread_id=log_message_thread_id
        )
    else:
        response = "<b>🔇 » Список забаненных людей:</b>\n"
        for idx, user in enumerate(banned_users, start=1):
            user_id, username, until_date, reason = user
            response += f"<blockquote><b>{idx}.</b> <a href='tg://user?id={user_id}'>{username}</a>\n<b>Выдано до:</b> <code>{until_date}</code>\n<b>Причина:</b> <code>{reason}</code></blockquote>\n\n"
        await message.answer(response, parse_mode='html')
        await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/banlist</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n"
            f"<b>✉️ Полученное сообщение:</b>"
            f"<blockquote>{response}</blockquote>",
            parse_mode="HTML", message_thread_id=log_message_thread_id
        )