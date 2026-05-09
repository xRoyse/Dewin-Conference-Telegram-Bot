from aiogram import types
from sqlalchemy.sql import text

from database.database import get_admin_level, async_session, get_user_info, get_user_level, get_marriage
from utils.loader import dew_channel, log_message_thread_id

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def profile_command_handler(bot, message: types.Message):
    group_id = message.chat.id  
    if message.reply_to_message:  
        target_user_id = message.reply_to_message.from_user.id
    else:
        target_user_id = message.from_user.id 
    
    user_info = await get_user_info(group_id, target_user_id) 
    admin_level = await get_admin_level(target_user_id, group_id)  

    if user_info:
        username = user_info['username'] if user_info['username'] else "Не указано"
        user_mention = f"<a href='tg://user?id={target_user_id}'>{username}</a>"
        
        message_count = user_info['sms']
        registration_date = user_info['data_reg']
        user_reputation = user_info['reputation']
        user_exp = user_info['exp']
        user_level = await get_user_level(user_exp)

        # Проверяем наличие брака
        marriage = await get_marriage(group_id,target_user_id)

        if marriage:
            spouse_id = marriage['user1_id'] if marriage['user2_id'] == target_user_id else marriage['user2_id']
            spouse = await bot.get_chat(spouse_id)
            spouse_mention = f"<a href='tg://user?id={spouse.id}'>{spouse.first_name}</a>"
            marriage_text = f"👥 Состоит в браке с {spouse_mention}"
        else:
            marriage_text = "👥 Не состоит в браке"

        if admin_level == 5:
            position = "Developer"
        elif admin_level == 4:
            position = "Основатель"
        elif admin_level == 3:
            position = "Администратор"
        elif admin_level == 2:
            position = "Модератор"
        elif admin_level == 1:
            position = "Мл. Модератор"
        else:
            position = None 

        if position:
            response_text = (
                f"<b>⚖️ » Профиль {user_mention}</b>\n\n"
                f"<b>👥 Группа: <code>{message.chat.title}</code></b>\n"
                f"<b>🛠 Должность: <code>{position}</code></b>\n\n"
                f"<b>{marriage_text}</b>\n\n"
                f"<b>✨ Репутация: <code>{user_reputation}</code></b>\n"
                f"<b>💠 Уровень: <code>{user_level} ({user_exp} опыта)</code></b>\n\n"
                f"<b>✉️ Количество сообщений: <code>{message_count}</code></b>\n"
                f"<b>📆 Добавлен в БД: <code>{registration_date}</code></b>"
            )
        else:
            response_text = (
                f"<b>⚖️ » Профиль {user_mention}</b>\n\n"
                f"<b>👥 Группа: <code>{message.chat.title}</code></b>\n\n"
                f"<b>{marriage_text}</b>\n\n"
                f"<b>✨ Репутация: <code>{user_reputation}</code></b>\n"
                f"<b>💠 Уровень: <code>{user_level} ({user_exp} опыта)</code></b>\n\n"
                f"<b>✉️ Количество сообщений: <code>{message_count}</code></b>\n"
                f"<b>📆 Добавлен в БД: <code>{registration_date}</code></b>"
            )
        
        # Кнопка "Информация о браке"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("📜 Информация о браке", callback_data=f"marriage_info:{target_user_id}:{group_id}"))

        await message.answer(response_text, parse_mode='HTML', reply_markup=keyboard)

        await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/profile</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n"
            f"<b>✉️ Полученное сообщение:</b>"
            f"<blockquote>{response_text}</blockquote>",
            parse_mode="HTML", message_thread_id=log_message_thread_id
        )
    else:
        await message.answer("Пользователь не найден в базе данных.")

async def marriage_info_callback(callback: types.CallbackQuery, user_id: int, group_id: int):
    _, user_id, group_id = callback.data.split(":")
    user_id, group_id = int(user_id), int(group_id)

    response_text = "" 

    marriage = await get_marriage(group_id, user_id)

    if marriage:
        spouse_id = marriage['user1_id'] if marriage['user2_id'] == user_id else marriage['user2_id']
        spouse = await callback.bot.get_chat(spouse_id)

        user1_id = marriage['user1_id']
        user2_id = marriage['user2_id']

        username1 = (await callback.bot.get_chat(marriage['user1_id'])).first_name
        username2 = (await callback.bot.get_chat(marriage['user2_id'])).first_name
        marriage_number = marriage['marriage_id']
        date_of_marriage = marriage['date_of_marriage']

        response_text = (
            f"<b>📜 » Информация о браке</b>\n\n"
            f"<b>#⃣ Номер брака: <code>{marriage_number}</code></b>\n\n"
            f"<b>👥 <a href='tg://user?id={user1_id}'>{username1}</a> женат на <a href='tg://user?id={user2_id}'>{username2}</a></b>\n\n"
            f"<b>🗓 Заключили брак: <code>{date_of_marriage}</code></b>"
        )
    else:
        user = await callback.bot.get_chat(user_id)
        response_text = (
            f"<b>🚫 {user.first_name}, Вы не находитесь в браке.>/b>\n"
            f"<b>Чтобы пожениться используйте команду:</b>\n"
            f"<blockquote>/wedding @user</blockquote>"
        )

    await callback.message.edit_text(response_text, parse_mode='HTML')
    await callback.answer()