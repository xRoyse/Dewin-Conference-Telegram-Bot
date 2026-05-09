from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import async_session, check_marriage, create_marriage
from sqlalchemy import text


async def wedding_message_handler(message: types.Message):
    user1_id = message.from_user.id
    group_id = message.chat.id

    args = message.text.split()
    if len(args) < 2 or not args[1].startswith('@'):
        await message.answer(
            "<b>💍 Для предложения брака укажите username партнера через @</b>\n\n"
            "<i>Пример:</i>\n<code>/wedding @username</code>", 
            parse_mode='HTML'
        )
        return

    user2_username = args[1][1:]

    async with async_session() as session:
        result = await session.execute(
            text("""
                SELECT u.user_id, u.username
                FROM memberships m
                JOIN users u ON u.user_id = m.user_id
                WHERE m.group_id = :group_id AND u.username = :username
            """),
            {"group_id": group_id, "username": user2_username}
        )
        user2_data = result.mappings().first()

        if not user2_data:
            await message.answer(
                "❌ <b>Пользователь не найден в этой группе.</b>",
                parse_mode='HTML'
            )
            return

        user2_id = user2_data['user_id']

        if await check_marriage(user1_id, group_id):
            await message.answer(
                "💔 <b>Вы уже состоите в браке в этой группе!</b>",
                parse_mode='HTML'
            )
            return

        if await check_marriage(user2_id, group_id):
            await message.answer(
                f"💔 <b>@{user2_username} уже состоит в браке!</b>",
                parse_mode='HTML'
            )
            return

        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("💍 Принять", callback_data=f"wedding_accept:{user1_id}:{user2_id}:{group_id}"),
            InlineKeyboardButton("🚫 Отказать", callback_data=f"wedding_decline:{user2_id}")
        )

        await message.answer(
            f"💌 <b>@{user2_username}, вам предложение руки и сердца от "
            f"<a href='tg://user?id={user1_id}'>{message.from_user.first_name}</a>!</b>\n\n"
            "Вы согласны стать супругом(ой)?",
            reply_markup=keyboard, 
            parse_mode='HTML'
        )


async def accept_wedding(callback: types.CallbackQuery, user1_id: int, user2_id: int, group_id: int):
    if callback.from_user.id != user2_id:
        await callback.answer("❌ Это предложение не для вас!", show_alert=True)
        return
    
    success = await create_marriage(user1_id, user2_id, group_id)

    if success:
        user1 = await callback.bot.get_chat(user1_id)
        user2 = await callback.bot.get_chat(user2_id)
        
        await callback.message.edit_text(
            f"🎉 <b>Поздравляем с бракосочетанием!</b>\n\n"
            f"💑 <a href='tg://user?id={user1_id}'>{user1.first_name}</a> + "
            f"<a href='tg://user?id={user2_id}'>{user2.first_name}</a>\n\n"
            f"💕 Желаем счастливой семейной жизни!",
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text("⚠️ Ошибка при заключении брака")


async def decline_wedding(callback: types.CallbackQuery, user2_id: int):
    if callback.from_user.id != user2_id:
        await callback.answer("❌ Это предложение не для вас!", show_alert=True)
        return

    await callback.message.edit_text(
        "💔 <b>Предложение брака было отклонено</b>",
        parse_mode="HTML"
    )