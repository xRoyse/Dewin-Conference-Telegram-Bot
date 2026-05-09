from aiogram import types
from database.database import get_all_users_in_group, get_group_info_from_db

async def group_command_handler(bot, message: types.Message):
    group_id = message.chat.id
    info = await get_group_info_from_db(group_id)
    if not info:
        await message.reply("Информация о группе не найдена в базе данных.")
        return

    # Название группы
    title = info.get('title', message.chat.title or "Без названия")

    # Получаем всех пользователей, реально находящихся в группе (is_member=True)
    users = await get_all_users_in_group(group_id)
    real_users = [u for u in users if u.get('is_member', True)]
    users_count = len(real_users)

    # Суммируем сообщения всех пользователей
    total_messages = sum(u.get('sms', 0) for u in real_users)

    # Дата основания
    created_at = info.get('created_at', '—')
    if created_at and created_at != '—':
        try:
            from datetime import datetime
            dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            created_at = dt.strftime("%H:%M %d:%m:%y")
        except Exception:
            pass

    # Основатель — пользователь с 4 уровнем админа
    owner = "—"
    for u in real_users:
        if u.get('admin_level', 0) == 4:
            username = u.get('username')
            if username:
                owner = f"<a href='https://t.me/{username}'>@{username}</a>"
            else:
                owner = f"<a href='tg://user?id={u.get('user_id')}'>{u.get('user_id')}</a>"
            break

    text = (
        f"<b>📘 Информация о группе</b>\n\n"
        f"<blockquote>📰 <b>Название:</b> <code>{title}</code>\n"
        f"👥 <b>Пользователей:</b> <code>{users_count}</code>\n"
        f"💬 <b>Сообщений:</b> <code>{total_messages}</code>\n"
        f"🗓 <b>Дата основания:</b> <code>{created_at}</code>\n\n"
        f"👑 <b>Основатель:</b> {owner}</blockquote>"
    )
    await message.reply(text, parse_mode="HTML", disable_web_page_preview=True)

async def group_users_command_handler(bot, message: types.Message):
    group_id = message.chat.id
    users = await get_all_users_in_group(group_id)
    if not users:
        await message.reply("В базе данных нет пользователей для этой группы.")
        return

    # Оставляем только тех, кто реально состоит в группе (is_member=True)
    real_users = [u for u in users if u.get('is_member', True)]
    if not real_users:
        await message.reply("В базе нет активных пользователей для этой группы.")
        return

    text = "<b>👥 Список пользователей группы:</b>\n\n"
    for i, user in enumerate(real_users, 1):
        username = user.get('username')
        user_id = user.get('user_id')
        if username:
            mention = f"@{username}"
        else:
            mention = f"<a href='tg://user?id={user_id}'>id:{user_id}</a>"
        text += f"{i}. {mention}\n"

    await message.reply(text, parse_mode="HTML", disable_web_page_preview=True)