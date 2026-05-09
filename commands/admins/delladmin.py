from aiogram import types
from sqlalchemy import text

from database.database import get_admin_level, async_session
from utils.loader import dew_channel, log_message_thread_id

async def delladmin_handlers(bot, message: types.Message):
    if len(message.text.split()) < 3:
        await message.reply("<blockquote>Использование: /delladmin «@тег» (уровень)</blockquote>", parse_mode="HTML")
        return

    command_args = message.text.split()
    username = command_args[1].replace('@', '')
    new_level = int(command_args[2])
    group_id = message.chat.id
    initiator = message.from_user

    # Проверка на попытку изменить свои права
    if username.lower() == initiator.username.lower():
        await message.reply("<b>⛔ Вы не можете изменять свой уровень администрирования.</b>", parse_mode="HTML")
        return

    initiator_level = await get_admin_level(initiator.id, group_id)
    if initiator_level < 3:
        await message.reply("<b>⛔ У вас недостаточно прав для снятия админов.</b>", parse_mode="HTML")
        return
    
    # Проверка на попытку понизить до своего или более высокого уровня
    if new_level >= initiator_level:
        await message.reply(f"<b>⛔ Вы не можете назначить уровень {new_level}, так как он равен или выше вашего текущего уровня администрирования.</b>", parse_mode="HTML")
        return

    async with async_session() as session:
        # Поиск пользователя по username в рамках группы
        result = await session.execute(
            text("""
                SELECT u.user_id, m.admin_level
                FROM memberships m
                JOIN users u ON u.user_id = m.user_id
                WHERE m.group_id = :group_id AND u.username = :username
            """),
            {"group_id": group_id, "username": username}
        )
        target_user = result.mappings().first()

        if not target_user:
            await message.reply(
                f"<b>⛔ Пользователь с тегом @{username} не найден в группе.</b>",
                parse_mode="HTML"
            )
            return

        current_target_level = target_user['admin_level']
        
        # Проверка на попытку повысить уровень (должна использоваться команда setadmin)
        if new_level > current_target_level:
            await message.reply(
                f"<b>⛔ Эта команда предназначена только для понижения уровня администрирования.\n\nДля повышения используйте /delladmin (текущий уровень администрирования: {current_target_level})</b>",
                parse_mode="HTML"
            )
            return

        # Обновляем admin_level
        await session.execute(
            text("""
                UPDATE memberships
                SET admin_level = :new_level
                WHERE group_id = :group_id AND user_id = :user_id
            """),
            {
                "new_level": new_level,
                "group_id": group_id,
                "user_id": target_user['user_id']
            }
        )
        await session.commit()

    await message.reply(f"<b>📉 Пользователь @{username} понижен на {new_level} уровень администрирования.</b>", parse_mode="HTML")
    await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/delladmin</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n"
            f"<b>✉️ Полученное сообщение:</b>"
            f"<blockquote>📉 Пользователь {username} понижен на {new_level} уровень администрирования</blockquote>",
            parse_mode="HTML", 
            message_thread_id=log_message_thread_id
            )