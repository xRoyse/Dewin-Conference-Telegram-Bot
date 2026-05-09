from aiogram import types

from database.database import get_stat

from utils.loader import dew_channel, log_message_thread_id

async def info_command_handler(bot, message: types.Message):
    print(f"Команда /info получена от пользователя {message.from_user.id} в группе {message.chat.id}")
    try:
        stats = await get_stat()
        group_count, user_count, sms_count = stats
        await message.reply(
            f"📊 <b>Информация о боте:</b>\n\n"
            f"⚙️ » <b>Версия:<code> 1.5</code></b>\n"
            f"🛡 » <b>Количество групп:</b> <code>{group_count} </code>\n"
            f"🎙 » <b>Количество пользователей в БД:</b> <code>{user_count} </code>\n"
            f"📨 » <b>Количество обработанных сообщений:</b> <code>{sms_count} </code>",
            parse_mode="HTML"
        )
        await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/info</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
            parse_mode="HTML", message_thread_id=log_message_thread_id
            )
    except Exception as e:
        print(f"Ошибка при получении статистики: {e}")
        await message.reply("❌ Произошла ошибка при получении информации. Попробуйте позже.")