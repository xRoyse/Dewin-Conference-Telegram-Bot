from aiogram import types
from sqlalchemy import text

from database.database import async_session, get_admins

from utils.loader import dew_channel, log_message_thread_id

async def admins_command_handler(bot, message: types.Message):
    group_id = message.chat.id
    developer = "Developer - @xRoyse"

    founders = await get_admins(group_id,4)
    admins = await get_admins(group_id,3)
    moderators = await get_admins(group_id,2)
    junior_mods = await get_admins(group_id,1)

    def format_admin_list(admin_list):
        if admin_list:
            return "\n".join([
                f"<b>• <a href='tg://user?id={user['user_id']}'>{user['username']}</a></b>"
                for user in admin_list
            ])
        return "<i>Нет пользователей</i>"

    response = f"""
<b>Список администраторов:</b>

👑 <b>Основатель:</b>
{format_admin_list(founders)}

💥 <b>Администратор:</b> 
{format_admin_list(admins)}

⚡ <b>Модератор:</b> 
{format_admin_list(moderators)}

🔥 <b>Мл. Модератор:</b> 
{format_admin_list(junior_mods)}
<blockquote><b>{developer}</b></blockquote>
    """
    await message.answer(response, parse_mode="HTML")
    await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/admins</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n"
            f"<b>✉️ Полученное сообщение:</b>"
            f"<blockquote>{response}</blockquote>",
            parse_mode="HTML", 
            message_thread_id=log_message_thread_id
            )