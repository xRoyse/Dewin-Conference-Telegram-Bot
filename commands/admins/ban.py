import asyncio
import logging
from aiogram import types
from datetime import datetime, timedelta

from sqlalchemy import text
from database.database import async_session, get_admin_level, ban_user, is_user_banned, unban_user
from utils.loader import dew_channel, log_message_thread_id
from aiogram.utils.exceptions import ChatAdminRequired

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def ban_handlers(bot, message: types.Message):
    admin_level = await get_admin_level(message.from_user.id, message.chat.id)
    
    if admin_level < 3:  # Требуем 3+ уровень админа
        await message.reply("<b>⛔ У вас недостаточно прав для использования этой команды.</b>", parse_mode="HTML")
        return
    
    if not message.reply_to_message:
        await message.reply("<b>⛔ Эта команда должна быть ответом на сообщение!</b>", parse_mode="HTML")
        return

    try:
        banint = int(message.text.split()[1])
        banetype = message.text.split()[2]
        reason = " ".join(message.text.split()[3:])
    except (IndexError, ValueError):
        await message.reply('<b>Не хватает аргументов или неверный формат!\n\nПример:</b>\n<blockquote>/бан 1 м причина</blockquote>', parse_mode='html')
        return

    # Устанавливаем время бана
    if banetype in ["д", "день", "дней"]:
        until_date = datetime.now() + timedelta(days=banint)
    elif banetype in ["с"]:
        until_date = datetime.now() + timedelta(days=banint / 1440)
    elif banetype in ["м", "месяц", "месяцев"]:
        until_date = datetime.now() + timedelta(days=banint * 30)
    else:
        await message.reply("Неверный тип времени. Используйте 'день' или 'месяц'.")
        return

    # Проверяем, Заблокирован ли пользователь
    group_name = message.chat.title
    user_id = message.reply_to_message.from_user.id
    user_admin_level = await get_admin_level(user_id, message.chat.id)
    username = message.reply_to_message.from_user.username or 'No username'

    if await is_user_banned(message.chat.id, user_id):
        await message.reply("<b>🚫 Этот пользователь уже Заблокирован.</b>", parse_mode='html')
        return

    # Проверяем, является ли пользователь участником группы
    try:
        member = await bot.get_chat_member(message.chat.id, user_id)
        if member.status in ['left', 'kicked']:
            await message.reply("<b>🚫 Этот пользователь уже покинул группу или был исключён.</b>", parse_mode='html')
            return
    except Exception as e:
        logging.error(f"Ошибка при проверке статуса пользователя: {e}")
        await message.reply("<b>❌ Не удалось проверить статус пользователя</b>", parse_mode='html')

    if not reason:
        await message.reply("<b>❌ Причина бана не может быть пустой.</b>", parse_mode='html')
        return
    
    if user_id == message.from_user.id:
        await message.reply("<b>❌ Вы не можете заблокировать самого себя.</b>", parse_mode='html')
        return

    # Проверяем, может ли пользователь заблокировать другого пользователя
    if user_admin_level > admin_level:
        await message.reply("<b>❌ Вы не можете заблокировать пользователя с более высоким уровнем админа.</b>", parse_mode='html')
        return

    # Баним пользователя
    await ban_user(group_name, message.chat.id, username, user_id, until_date.strftime('%Y-%m-%d %H:%M:%S'), reason)
    await bot.send_message(
        dew_channel, 
        f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
        f"<b>👤 Администратор <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> заблокировал пользователя <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a></b>"
        f"<blockquote><b>Дата разблокировки:</b> <code>{until_date.strftime('%H:%M %d-%m-%Y')}</code>\n"
        f"<b>Причина:</b> <code>{reason}</code></blockquote>\n"
        f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
        parse_mode="HTML", message_thread_id=log_message_thread_id
    )

    # Отправляем личное сообщение пользователю
    try:
        await bot.send_photo(
            chat_id=user_id,
            photo=open('media/photos/Заблокирован.png', 'rb'),
            caption=(
                f"<b>Вам выдали блокировку в группе <code>{message.chat.title}</code></b>\n\n"
                f"<b>Выдал:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n"
                f"<b>Разбан:</b> <code>{until_date.strftime('%H:%M %d-%м-%Y')}</code>\n\n"
                f"<b>Причина:</b> <code>{reason}</code>"
            ), parse_mode='html'
        )
    except Exception as e:
        logging.error(f"Не удалось отправить личное сообщение пользователю {user_id}: {e}")

    # Дополнительное сообщение для подтверждения
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=open('media/photos/Заблокирован.png', 'rb'),
        caption=(
            f"<b>Пользователь <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> был заблокирован.</b>\n\n"
            f"<b>Дата:</b> <code>{datetime.now().strftime('%H:%M %d-%м-%Y')}</code>\n"
            f"<b>Выдал: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a></b>\n"
            f"<b>Разбан:</b> <code>{until_date.strftime('%H:%M %d-%м-%Y')}</code>\n\n"
            f"<b>Причина:</b> <code>{reason}</code>"
        ), parse_mode='html'
    )

    # Кикаем пользователя
    try:
        await bot.kick_chat_member(message.chat.id, user_id, until_date=until_date)
    except ChatAdminRequired:
        await message.reply("❌ Я не могу забанить пользователя, так как не являюсь администратором или у меня нет права 'Банить участников'.")
    except Exception as e:
        await message.reply(f"❌ Ошибка при бане пользователя: {e}")

async def check_unban(bot):
    while True:
        await asyncio.sleep(60)  # Проверяем каждую минуту
        now = datetime.now()
        
        async with async_session() as session:
            query = '''
            SELECT * FROM ban_users WHERE until_date < :now
            '''
            result = await session.execute(text(query), {"now": now.strftime('%H:%M %Y-%m-%d')})
            ban_users = result.fetchall()

            for user in ban_users:
                group_id = user.group_id
                user_id = user.user_id
                username = user.username
                group_name = user.group_name

                # Удаляем пользователя из списка Заблокированных
                await unban_user(group_id, user_id)
                await bot.send_message(
                    dew_channel,
                    f"<b>👥  Группа: <code>{group_name}</code></b>\n\n"
                    f"<b>👤 C пользователя <a href='tg://user?id={user_id}'>{username}</a> была снята блокировка в группе</b>\n"
                    f"<b>💠 id пользователя: <code>{user_id}</code></b>\n\n",
                    parse_mode="HTML", message_thread_id=log_message_thread_id
                )

                # Отправляем сообщение пользователю о разблокировке
                try:
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=open('media/photos/Разблокирован.png', 'rb'),
                        caption=(
                            f"<b>❗️ С вас была снята блокировка в группе</b> <code>{group_name}</code>\n\n"
                            f"<b>⚠️ Теперь вы вновь можете вступить в группу и общаться, больше не нарушайте!</b>"
                        ), parse_mode='html'
                    )
                except Exception as e:
                    logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")