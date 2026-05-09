from datetime import datetime
from aiogram import types

from database.database import add_group_record, add_user_record, add_membership_record
from utils.loader import dew_channel, log_message_thread_id

async def reg_command_handler(bot, message: types.Message):
    if message.chat.type not in ['group', 'supergroup']:
        await message.reply("Команда /reg доступна только в группах.")
        return

    group_id = message.chat.id
    table_created = await add_group_record(group_id,message.chat.title)

    if table_created:

        data_reg = datetime.now().strftime('%H:%M %d-%m-%Y')

        founder_id = 1302525645
        founder_username = "xRoyse"
        await add_user_record(founder_id, founder_username)
        await add_membership_record(
            group_id=group_id,
            user_id=founder_id,
            admin_level=5,
            data_reg=data_reg
        )

        await add_user_record(message.from_user.id, message.from_user.username)
        await add_membership_record(group_id, message.from_user.id, 4, 0, 0, 0, data_reg)

        await message.reply(
            f"<b>Группа <code>'{message.chat.title}'</code> зарегистрирована.</b>\n"
            f"<blockquote>Вы теперь Основатель (уровень 4).</blockquote>\n\n"
            "🔗 <a href='https://dewinbot.ru/commands'>Список всех команд бота</a>",
            parse_mode="HTML"
        )
        await bot.send_message(
            dew_channel, 
           f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> зарегистрировал группу в БД</b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
            parse_mode="HTML", message_thread_id=log_message_thread_id
            )
    else:
        await message.reply("<b>❌ Группа уже зарегистрирована.</b>", parse_mode="HTML")