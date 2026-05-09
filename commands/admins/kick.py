import logging
from aiogram import types
from datetime import datetime

from database.database import get_admin_level, remove_membership_record
from utils.loader import dew_channel, log_message_thread_id

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def kick_handler(bot, message: types.Message):
    admin_level = await get_admin_level(message.from_user.id, message.chat.id)
    
    if admin_level < 1: 
        await message.reply("<b>⛔ У вас недостаточно прав для использования этой команды.</b>", parse_mode="HTML")
        return
    
    if not message.reply_to_message:
        await message.reply("<b>⛔ Эта команда должна быть ответом на сообщение!</b>", parse_mode="HTML")
        return

    try:
        reason = " ".join(message.text.split()[1:])
    except (IndexError, ValueError):
        await message.reply('<b>Не хватает аргументов или неверный формат!\n\nПример:</b>\n<blockquote>/кик причина</blockquote>', parse_mode='html')
        return

    user_id = message.reply_to_message.from_user.id
    user_admin_level = await get_admin_level(user_id, message.chat.id)

    try:
        member = await bot.get_chat_member(message.chat.id, user_id)
        if member.status in ['left', 'kicked']:
            await message.reply("<b>🚫 Этот пользователь уже покинул группу или был исключён.</b>", parse_mode='html')
            return
    except Exception as e:
        logging.error(f"Ошибка при проверке статуса пользователя: {e}")
        await message.reply("<b>❌ Не удалось проверить статус пользователя</b>", parse_mode='html')

    if not reason:
        await message.reply("<b>❌ Причина кика не может быть пустой.</b>", parse_mode='html')
        return
    
    if user_id == message.from_user.id:
        await message.reply("<b>❌ Вы не можете кикнуть самого себя.</b>", parse_mode='html')
        return

    # Проверяем, может ли пользователь заблокировать другого пользователя
    if user_admin_level > admin_level:
        await message.reply("<b>❌ Вы не можете кикнуть пользователя с более высоким уровнем админа.</b>", parse_mode='html')
        return

    await  bot.kick_chat_member(message.chat.id, user_id)
    await remove_membership_record(message.chat.id, user_id)
    await bot.send_message(
        dew_channel, 
        f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
        f"<b>👤 Администратор <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> кикнул из группы пользователя <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a></b>"
        f"<blockquote><b>Причина:</b> <code>{reason}</code></blockquote>\n"
        f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
        parse_mode="HTML", message_thread_id=log_message_thread_id
    )

    # Отправляем личное сообщение пользователю
    try:
        await bot.send_photo(
            chat_id=user_id,
            photo=open('media/photos/Кикнут.png', 'rb'),
            caption=(
                f"<b>Вас кикнули из группы <code>{message.chat.title}</code></b>\n\n"
                f"<b>Кикнул:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n"
                f"<b>Причина:</b> <code>{reason}</code>"
            ), parse_mode='html'
        )
    except Exception as e:
        logging.error(f"Не удалось отправить личное сообщение пользователю {user_id}: {e}")

    # Дополнительное сообщение для подтверждения
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=open('media/photos/Кикнут.png', 'rb'),
        caption=(
            f"<b>Пользователь <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> был кикнут из группы.</b>\n\n"
            f"<b>Дата:</b> <code>{datetime.now().strftime('%H:%M %d-%m-%Y')}</code>\n"
            f"<b>Кикнул: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a></b>\n"
            f"<b>Причина:</b> <code>{reason}</code>"
        ), parse_mode='html'
    )