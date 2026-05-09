from aiogram import types
from database.database import get_admin_level, get_muted_users 
from utils.loader import dew_channel, log_message_thread_id

async def mutelist_handler(bot, message: types.Message):
    group_id = message.chat.id
    muted_users = await get_muted_users(group_id)
    initiator_level = await get_admin_level(message.from_user.id, group_id)
    
    if initiator_level < 1:
        await message.reply("<b>⛔ У вас недостаточно прав для использования этой команды.</b>", parse_mode="HTML")
        return
    
    if not muted_users:
        await message.answer("<b>В вашей группе нет замьюченых людей, это круто! 😊</b>", parse_mode='html')
        await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/mutelist</code></b>\n"
            f"<b>✉️ Полученное сообщение:</b>"
            f"<blockquote><b>В вашей группе нет замьюченых людей, это круто! 😊</b></blockquote>",
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n",
            parse_mode="HTML", message_thread_id=log_message_thread_id
        )
    else:
        response = "<b>🔇 » Список замьюченых людей:</b>\n\n"
        for idx, user in enumerate(muted_users, start=1):
            user_id, username, until_date, comment = user
            response += f"<blockquote><b>{idx}.</b> <a href='tg://user?id={user_id}'>{username}</a>\n<b>Выдано до:</b> <code>{until_date}</code>\n<b>Причина:</b> <code>{comment}</code></blockquote>\n\n"
        await message.answer(response, parse_mode='html')
        await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/mutelist</code></b>\n"
             f"<b>✉️ Полученное сообщение:</b>"
            f"<blockquote>{response}</blockquote>",
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n",
            parse_mode="HTML", message_thread_id=log_message_thread_id
        )