from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.loader import dew_channel, log_message_thread_id

async def private_welcome_messenge_handler(bot, message, user_id, username):
    if message.chat.type != "private":
        await message.reply("Эта команда доступна только в личных сообщениях с ботом.")
        return

    if user_id == 1302525645:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(KeyboardButton("🛡 Добавить бота в чат"))
        keyboard.row(KeyboardButton("📁 О проекте"), KeyboardButton("🔗 Команды")) 
        keyboard.row(KeyboardButton("🛠 Тех. поддержка"))
        keyboard.row(KeyboardButton("💙 Dewin Team"))
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(KeyboardButton("🛡 Добавить бота в чат"))
        keyboard.row(KeyboardButton("📁 О проекте"), KeyboardButton("🔗 Команды")) 
        keyboard.row(KeyboardButton("🛠 Тех. поддержка"))

    await bot.send_photo(
            chat_id=message.chat.id,
            photo=open('media/photos/привет.png', 'rb'),
            caption=(
                f"<b>Привет <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>!</b>\n\n"
                f"Я <code>Dewin » ConferenceBot</code> и могу тебе помочь с возможностью модерирования группы, удобного информирования пользователей, а так же принесу вам в группу развлечения!\n\n"
                f"Если стало инересно, подробнее можешь узнать по кнопкам в клавиатуре 💙"
            ), reply_markup=keyboard, parse_mode='HTML'
        )

    await bot.send_message(
        dew_channel,
        f"Пользователь <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a> включил уведомления в боте.\nID пользователя: <code>{user_id}</code>",
        parse_mode="HTML",
        message_thread_id=log_message_thread_id
    )