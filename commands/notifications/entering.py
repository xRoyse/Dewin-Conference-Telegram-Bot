from datetime import datetime

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.database import get_admin_level, get_ban_info, is_user_banned, unban_user
from utils.loader import dew_channel, log_message_thread_id

async def send_group_welcome(bot, message, user, add_user, add_membership):
    group_name = message.chat.title
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

    await bot.send_message(
        dew_channel,
        f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
        f"<b>👤 Пользователь <a href='tg://user?id={user.id}'>{user.first_name}</a> присоеденился к группе</b>\n"
        f"<b>💠 id пользователя: <code>{user.id}</code></b>\n\n",
        parse_mode="HTML", message_thread_id=log_message_thread_id
    )

    # Проверяем, забанен ли пользователь
    if await is_user_banned(message.chat.id, user.id):
        # Получаем информацию о бане
        until_date, reason = await get_ban_info(message.chat.id, user.id)

        # Кикаем пользователя
        await bot.kick_chat_member(message.chat.id, user.id)

        # Создаем клавиатуру с кнопкой "разбанить"
        keyboard = InlineKeyboardMarkup()
        unban_button = InlineKeyboardButton("Разбанить", callback_data=f"unban_{user.id}_{message.chat.id}")
        keyboard.add(unban_button)

        # Отправляем сообщение о бане с кнопкой
        await message.answer(
            f"<b>🚫 Пользователь {mention} заблокирован!</b>\n\n"
            f"<blockquote><b>Причина:</b> <code>{reason}</code>\n"
            f"<b>Разблокировка:</b> <code>{until_date}</code></blockquote>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        return  # Выходим из функции, чтобы не отправлять приветственное сообщение

    # Если пользователь не забанен, отправляем приветственное сообщение
    if user.is_bot and user.id == 7803753519:
        await bot.send_message(
            message.chat.id,
            "💙 <b>Спасибо, что добавили меня в группу!\n\nЯ готов к работе, но перед этим, Вы должны меня зарегистрировать тут с помощью команды /reg</b>",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"👋 » Добро пожаловать в <b><code>{group_name}</code></b>\n\n"
            f"💞 » Спасибо, что присоединился к нашей группе. Мы тебя любим.\n\n"
            f"Отправлено пользователю {mention}",
            parse_mode="HTML"
        )

    date_registered = datetime.now().strftime('%H:%M %d-%m-%Y')
    await add_user(user.id,user.username)
    await add_membership(message.chat.id, user.id,admin_level=0,data_reg=date_registered,exp=0,reputation=0)

    if add_user:
        await bot.send_message(
            dew_channel,
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> добавлен в БД</b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
            parse_mode="HTML", message_thread_id=log_message_thread_id
        )


async def unban_user_handler(bot, message, callback_query: types.CallbackQuery):
    user_id, chat_id = map(int, callback_query.data.split("_")[1:3])

    admin_level = await get_admin_level(callback_query.from_user.id, chat_id)

    if admin_level < 3:
        await callback_query.answer("⛔ У вас недостаточно прав для разблокировки пользователя.")
        return

    await unban_user(chat_id, user_id)
    
    if callback_query.message.reply_to_message:
        reply_user_first_name = callback_query.message.reply_to_message.from_user.first_name
    else:
        reply_user_first_name = "ранее заблокированного"

    await callback_query.message.answer(
        text=(
            f"<b>Пользователь был разбанен!</b>\n"
            f"<b>Разбанил: <a href='tg://user?id={callback_query.from_user.id}'>{callback_query.from_user.first_name}</a></b>"
        ), parse_mode="HTML")
    
    await bot.send_message(
        dew_channel, 
        f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
        f"<b>👤 Администратор <a href='tg://user?id={callback_query.from_user.id}'>{callback_query.from_user.first_name}</a> разбанил <a href='tg://user?id={user_id}'>{reply_user_first_name}</a> пользователя используя кнопку в приветственном сообщении</b>\n"
        f"<b>💠 id пользователя: <code>{callback_query.from_user.id}</code></b>\n\n",
        parse_mode="HTML", message_thread_id=log_message_thread_id
    )

async def send_left_member(bot, message, remove_membership_record):
    await message.reply(f'Пока, <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>, надеемся еще увидимся! 😔', parse_mode="HTML") 
    user_left = await remove_membership_record(message.chat.id, message.from_user.id)
    if user_left:
        await bot.send_message(
            dew_channel,
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> вышел из группы</b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
            parse_mode="HTML", message_thread_id=log_message_thread_id
        )