from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher
from database.database import async_session, check_marriage, get_username_by_id
from sqlalchemy import text

# Хендлер команды для инициации развода
async def divorce_messege_handler(message: types.Message):
    user_id = message.from_user.id
    group_id = message.chat.id

    marriage_id = await check_marriage(user_id, group_id)

    if marriage_id:
        async with async_session() as session:
            query = f'SELECT user1_id, user2_id FROM marriages WHERE marriage_id = {marriage_id} AND group_id = {group_id}'
            result = await session.execute(text(query))
            marriage = result.mappings().all()

            if marriage:
                user1_id = marriage[0]['user1_id']
                user2_id = marriage[0]['user2_id']

                if user_id in (user1_id, user2_id):
                    spouse_id = user2_id if user_id == user1_id else user1_id
                    spouse_username = await get_username_by_id(spouse_id, group_id)

                    # Создаем инлайн клавиатуру с кнопками
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(
                        InlineKeyboardButton("✅ Да", callback_data=f"divorce_confirm:{marriage_id}:{group_id}"),
                        InlineKeyboardButton("❌ Нет", callback_data="divorce_cancel")
                    )

                    await message.answer(
                        f"⁉️ <b>Вы действительно хотите расторгнуть брак с <a href='tg://user?id={spouse_id}'>{spouse_username}</a></b>?\n\nВ случае если да, то ваш брак будет сразу расторгнут.",
                        parse_mode="HTML", reply_markup=keyboard
                    )
                    return

            await message.answer("❗ Брак не найден.")
    else:
        await message.answer("❗ Вы не состоите в браке, чтобы расторгнуть его.")

# Хендлер для кнопки "Да"
async def accept_divorce(callback: types.CallbackQuery, marriage_id: int, group_id: int):
    from_user = callback.from_user.id

    async with async_session() as session:
        query = f'SELECT user1_id, user2_id FROM marriages WHERE marriage_id = {marriage_id} AND group_id = {group_id}'
        result = await session.execute(text(query))
        marriage = result.mappings().first()

        if not marriage:
            await callback.message.edit_text("❗ Брак не найден.")
            return

        user1_id, user2_id = marriage.user1_id, marriage.user2_id

        if from_user not in (user1_id, user2_id):
            await callback.message.edit_text("❗ Это не ваш брак.")
            return

        # Удаляем брак
        delete_query = f'DELETE FROM marriages WHERE marriage_id = {marriage_id}'
        await session.execute(text(delete_query))
        await session.commit()

        spouse_id = user2_id if from_user == user1_id else user1_id
        user = await callback.bot.get_chat(from_user)
        spouse = await callback.bot.get_chat(spouse_id)

        await callback.message.edit_text(
            f"<b>💔 По инициативе <a href='tg://user?id={user.id}'>{user.first_name}</a> брак с <a href='tg://user?id={spouse.id}'>{spouse.first_name}</a> был расторгнут</b>",
            parse_mode="HTML"
        )

# Хендлер для кнопки "Нет"
async def cancel_divorce(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("<b>🗒 Расторжение брака отменено.</b>",
            parse_mode="HTML")