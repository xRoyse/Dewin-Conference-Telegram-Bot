from aiogram import types
from sqlalchemy import text
from database.database import async_session, get_admin_level, get_all_users_in_group
from utils.loader import dew_channel, log_message_thread_id

async def mention_all_members_handlers(bot, message: types.Message):
    group_id = message.chat.id
    initiator_level = await get_admin_level(message.from_user.id, group_id)
    
    if initiator_level < 1:
        await message.reply("<b>⛔ У вас недостаточно прав для использования этой команды.</b>", parse_mode="HTML")
        return

    users_in_group = await get_all_users_in_group(group_id)

    mentions = []
    for user in users_in_group:
        user_id = user['user_id']
        username = user['username'] or f"Пользователь {user_id}"

        mention = f"<b><i><a href='tg://user?id={user_id}'>{username}</a></i></b>"
        mentions.append(mention)

    if not mentions:
        await message.answer("В группе нет пользователей для упоминания.")
        return

    mention_text = ", ".join(mentions)
    notification_text = (
        f"<b>Dewin » Упоминание всех участников группы</b>\n\n"
        f"{mention_text}"
    )

    sent_message = await message.answer(notification_text, parse_mode="HTML")

    log_message = (
        f"<b>👥 Группа: <code>{message.chat.title}</code></b>\n\n"
        f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> "
        f"использовал команду <code>/all</code></b>\n"
        f"<b>💠 ID пользователя: <code>{message.from_user.id}</code></b>\n\n"
        f"<b>✉️ Отправленное упоминание:</b>\n"
        f"<blockquote>{notification_text}</blockquote>"
    )

    await bot.send_message(
        dew_channel,
        log_message,
        parse_mode="HTML",
        message_thread_id=log_message_thread_id
    )