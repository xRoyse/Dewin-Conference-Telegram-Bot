from aiogram import types
from database.database import get_admin_level, unban_user, is_user_banned
from utils.loader import dew_channel, log_message_thread_id

async def unban_handlers(bot, message: types.Message):
    # Получаем уровень администратора
    admin_level = await get_admin_level(message.from_user.id, message.chat.id)
    
    # Проверяем, является ли пользователь администратором
    if admin_level < 3:  # Предполагаем, что уровень администратора >= 1
        await message.reply("<b>⛔ У вас недостаточно прав для использования этой команды.</b>", parse_mode="HTML")
        return

    if not message.reply_to_message:
        # Проверка на наличие упоминания
        if len(message.text.split()) < 2:
            await message.reply("Неверный формат команды\nИспользуйте:\n<code>/unban (ответ на сообщение)</code>", parse_mode='HTML')
            return
        # Попробуем получить упоминание пользователя
        try:
            mentioned_user = message.text.split()[1]
            user_id = int(mentioned_user[1:-1])  # Извлекаем ID пользователя из упоминания
        except (ValueError, IndexError):
            await message.reply("Неверный формат команды\nИспользуйте:\n<code>/unban (ответ на сообщение)</code>", parse_mode='HTML')
            return
    else:
        user_id = message.reply_to_message.from_user.id  # Если команда была ответом на сообщение

    # Проверяем, забанен ли пользователь
    if not await is_user_banned(message.chat.id, user_id):
        await message.reply("Этот пользователь не забанен.")
        return

    # Снимаем бан у пользователя
    await unban_user(message.chat.id, user_id)
    await bot.send_message(
        dew_channel, 
        f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
        f"<b>👤 Администратор <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> разблокировал пользователя <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a></b>\n"
        f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
        parse_mode="HTML", message_thread_id=log_message_thread_id
    )

    # Уведомляем о снятии бана в группу
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=open('media/photos/Разблокирован.png', 'rb'),
        caption=(
            f"<b>Пользователь <a href='tg://user?id={user_id}'>{message.reply_to_message.from_user.first_name}</a> был разбанен.</b>\n"
            f"<b>Разбанил: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a></b>"
        ), parse_mode='HTML'
    )

    # Отправляем личное сообщение пользователю
    try:
        await bot.send_photo(
            chat_id=user_id,
            photo=open('media/photos/Разблокирован.png', 'rb'),
            caption=(
                f"<b>Вам сняли бан в группе {message.chat.title}.</b>\n"
                f"<b>Разбанил: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a></b>"
            ), parse_mode='HTML'
        )
    except Exception as e:
        # Логируем ошибку или просто пропускаем
        print(f"Не удалось отправить личное сообщение пользователю {user_id}: {e}")
