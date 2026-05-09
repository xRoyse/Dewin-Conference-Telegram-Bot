from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import text

from database.database import async_session, add_message

async def send_mention_message_handlers(message: types.Message, bot):
    group_id = message.chat.id
    sender = message.from_user
    sms_text = message.text[5:].strip()

    async with async_session() as session:
        query = text("""
            SELECT u.user_id, u.username, m.admin_level
            FROM memberships m
            JOIN users u ON u.user_id = m.user_id
            WHERE m.group_id = :group_id
        """)
        result = await session.execute(query, {"group_id": group_id})
        users_in_group = result.mappings().all()

        admin_level = next((user['admin_level'] for user in users_in_group if user['user_id'] == sender.id), 0)
        if admin_level < 1:
            await message.reply("У вас недостаточно прав для отправки сообщений.")
            return

        if not sms_text or sms_text.lower() == "dewinconferencebot":
            await message.answer(
                "<b>Уверены, что хотите отправить пустое сообщение?\n<blockquote>Пример использования команды: <code>/sms текст</code></blockquote></b>",
                reply_markup=InlineKeyboardMarkup(row_width=2).add(
                    InlineKeyboardButton("Да", callback_data=f'confirm_send_empty:{group_id}:{sender.id}'),
                    InlineKeyboardButton("Нет", callback_data='cancel_send'),
                ),
                parse_mode="HTML"
            )
            return

        mentioned_users = message.reply_to_message.entities if message.reply_to_message else []
        user_ids_to_message = []
        mentions_list = []

        if mentioned_users:
            for entity in mentioned_users:
                if entity.type == 'mention':
                    username = entity.user.username
                    target_user = next((user for user in users_in_group if user['username'] == username), None)
                    if target_user:
                        user_ids_to_message.append(target_user['user_id'])
                        mentions_list.append(f"<a href='tg://user?id={target_user['user_id']}'>{username}</a>")
        else:
            user_ids_to_message = [user['user_id'] for user in users_in_group]
            mentions_list = [f"<a href='tg://user?id={user['user_id']}'>{user['username'] or user['user_id']}</a>" for user in users_in_group]

        group_name = message.chat.title
        current_time = message.date.strftime('%H:%M %d-%m-%Y')
        has_photo = message.reply_to_message.photo if message.reply_to_message else None

        notification_text = (
            f"🔔 <b>Dewin » Уведомление\n\n"
            f"Группа:</b> <code>{group_name}</code>\n"
            f"<b>Время:</b> <code>{current_time}</code>\n"
            f"<b>Отправитель:</b> <a href='tg://user?id={sender.id}'>{sender.first_name}</a>\n\n"
            f"<b>Сообщение:</b> <code>{sms_text}</code>"
        )

        command_link = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Включить уведомления", url='https://t.me/DewinConferenceBot?start=start')
        )

        delivered_users = []
        undelivered_users = []

        for user_id in user_ids_to_message:
            try:
                if has_photo:
                    await bot.send_photo(user_id, photo=has_photo[-1].file_id, caption=notification_text, parse_mode="HTML")
                else:
                    await bot.send_message(user_id, notification_text, parse_mode="HTML")
                delivered_users.append(user_id)
                await add_message(group_id, user_id)
            except Exception:
                undelivered_users.append(user_id)

        delivered_mentions = [
            f"<a href='tg://user?id={user['user_id']}'>{user['username'] or user['user_id']}</a>"
            for user in users_in_group if user['user_id'] in delivered_users
        ]
        undelivered_mentions = [
            f"<a href='tg://user?id={user['user_id']}'>{user['username'] or user['user_id']}</a> 🔇"
            for user in users_in_group if user['user_id'] in undelivered_users
        ]

        all_mentions = delivered_mentions + undelivered_mentions

        response = (
            f"<b>Dewin » Упоминание пользователей:</b>\n\n"
            f"Упомянутые: {', '.join(all_mentions) if all_mentions else 'Нет пользователей'}\n"
            f"Упомянул: <a href='tg://user?id={sender.id}'>{sender.first_name}</a>\n\n"
            f"<b>Сообщение:</b> <code>{sms_text or 'Пусто'}</code>\n\n"
            f"<b>🔇 - Не получил сообщение (не включил в боте)</b>"
        )

        await message.answer(response, parse_mode="HTML", reply_markup=command_link)

async def process_confirm_send_empty(call: types.CallbackQuery, bot):
    _, group_id, sender_id = call.data.split(':')
    group_id = int(group_id)
    sender_id = int(sender_id)

    async with async_session() as session:
        query = text("""
            SELECT u.user_id, u.username
            FROM memberships m
            JOIN users u ON u.user_id = m.user_id
            WHERE m.group_id = :group_id
        """)
        result = await session.execute(query, {"group_id": group_id})
        users_in_group = result.mappings().all()

        group_name = call.message.chat.title
        current_time = call.message.date.strftime('%H:%M %d-%m-%Y')

        notification_text = (
            f"🔔 <b>Dewin » Уведомление\n\n"
            f"Группа:</b> <code>{group_name}</code>\n"
            f"<b>Время:</b> <code>{current_time}</code>\n"
            f"<b>Отправитель:</b> <a href='tg://user?id={call.from_user.id}'>{call.from_user.first_name}</a>\n\n"
            f"<b>Сообщение:</b> <code>Пусто</code>"
        )

        delivered_users = []
        undelivered_users = []

        for user in users_in_group:
            try:
                await bot.send_message(user['user_id'], notification_text, parse_mode="HTML")
                delivered_users.append(user['user_id'])
                await add_message(group_id, user['user_id'])
            except Exception:
                undelivered_users.append(user['user_id'])

        all_mentions = [
            f"<a href='tg://user?id={user['user_id']}'>{user['username'] or user['user_id']}</a>"
            + (" 🔇" if user['user_id'] in undelivered_users else "")
            for user in users_in_group
        ]

        response = (
            f"<b>Dewin » Упоминание пользователей:</b>\n\n"
            f"Упомянутые: {', '.join(all_mentions) if all_mentions else 'Нет пользователей'}\n"
            f"Упомянул: <a href='tg://user?id={call.from_user.id}'>{call.from_user.first_name}</a>\n\n"
            f"<b>Сообщение:</b> <code>Пусто</code>\n\n"
        )

        command_link = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Включить уведомления", url='https://t.me/DewinConferenceBot?start=start')
        )

        await call.message.edit_text(response, parse_mode="HTML", reply_markup=command_link)

async def cancel_send(call: types.CallbackQuery):
    await call.message.edit_text("Отправка сообщения отменена.")