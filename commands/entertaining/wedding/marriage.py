from aiogram import types
from database.database import async_session
from sqlalchemy import text
from utils.loader import dew_channel, log_message_thread_id

async def marriage_message_handler(bot, message: types.Message):
    group_id = message.chat.id

    async with async_session() as session:
        result = await session.execute(
            text("""
                SELECT m.marriage_id, m.user1_id, m.user2_id, m.date_of_marriage,
                       u1.username as user1_username, u2.username as user2_username
                FROM marriages m
                JOIN users u1 ON m.user1_id = u1.user_id
                JOIN users u2 ON m.user2_id = u2.user_id
                WHERE m.group_id = :group_id
            """),
            {"group_id": group_id}
        )
        marriages = result.mappings().all()

    if marriages:
        marriage_list = []
        for marriage in marriages:
            user1_link = f"<a href='tg://user?id={marriage['user1_id']}'>{marriage['user1_username']}</a>"
            user2_link = f"<a href='tg://user?id={marriage['user2_id']}'>{marriage['user2_username']}</a>"
            marriage_list.append(f"▹ <b>{user1_link} женат на {user2_link}</b>")
        
        response = [
            "<b>👥 » Список браков в беседе</b>",
            "",
            "<blockquote>" + "\n".join(marriage_list) + "</blockquote>",
            "",
            "<b>Чтобы зарегистрировать новый брак используйте команду:</b>",
            "<blockquote>/wedding @username</blockquote>"
        ]

        await message.answer(
            "\n".join(response),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "<b>👥 » Список браков в беседе</b>\n\n"
            "<blockquote>😕 В беседе не было зарегистрировано бракосочетаний.</blockquote>\n\n"
            "<b>Чтобы зарегистрировать новый брак используйте команду:</b>\n"
            "<blockquote>/wedding @username</blockquote>",
            parse_mode="HTML"
        )
        await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/marriage</code></b>\n"
            f"<b>💬 Полученное сообщение: <blockquote><b>👥 » Список браков в беседе</b>\n\n😕 В беседе не было зарегистрировано бракосочетаний.</blockquote></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
            parse_mode="HTML", message_thread_id=log_message_thread_id
            )