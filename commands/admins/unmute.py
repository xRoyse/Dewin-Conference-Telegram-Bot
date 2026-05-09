from aiogram import types
from database.database import get_admin_level, unmute_user, is_user_muted
from utils.loader import dew_channel, log_message_thread_id

async def unmute_handlers(bot, message: types.Message):
    admin_level = await get_admin_level(message.from_user.id, message.chat.id)
    
    if admin_level < 2:  
        await message.reply("<b>⛔ У вас недостаточно прав для использования этой команды.</b>", parse_mode="HTML")
        return

    if not message.reply_to_message:
        if len(message.text.split()) < 2:
            await message.reply("<b>⛔ Неверный формат команды\n\nИспользуйте:</b>\n<code>/blockquote (ответ на сообщение)</blockquote>", parse_mode='html')
            return
        
        try:
            mentioned_user = message.text.split()[1]
            user_id = int(mentioned_user[1:-1])  
        except (ValueError, IndexError):
            await message.reply("<b>⛔ Неверный формат команды!\n\nИспользуйте:</b>\n<blockquote>/unmute (ответ на сообщение)</blockquote>", parse_mode='html')
            return
    else:
        user_id = message.reply_to_message.from_user.id 
        
    if not await is_user_muted(message.chat.id, user_id):
        await message.reply("<b>⛔ Этот пользователь не замьючен!</b>", parse_mode='html')
        return

    await unmute_user(message.chat.id, user_id)
    await bot.send_message(
        dew_channel, 
        f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
        f"<b>👤 Администратор <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> разблокировал чат (размутил) пользователя <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a></b>\n"
        f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
        parse_mode="HTML", message_thread_id=log_message_thread_id
    )

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=open('media/photos/Размьючен.png', 'rb'),
        caption=(
            f"<b>❗️ Пользователю <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> была снята блокировка чата.</b>\n"
            f"<b>✅ Снял: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a></b>"
        ),
        parse_mode='HTML'
    )

    try:
        await bot.send_photo(
            chat_id=user_id,
            photo=open('media/photos/Размьючен.png', 'rb'),
            caption=(
                f"<b>❗️ Вам сняли блокировку чата в группе <code>{message.chat.title}</code></b>\n\n"
                f"<b>✅ Снял: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a></b>\n\n"
                f"<b>⚠️ Теперь вы вновь можете писать, больше не нарушайте!</b>"
            ), parse_mode='html'
        )
    except Exception as e:
        print(f"Не удалось отправить личное сообщение пользователю {user_id}: {e}")
