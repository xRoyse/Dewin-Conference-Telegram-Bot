import os
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.texts import invite, project, commands, tex
from commands.private.start import private_welcome_messenge_handler
from support.handlers.client import client_start, client_newquestion, handler_button_new_question

async def private_message_handler(bot, message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    text = message.text

    if text == "/start":
        await private_welcome_messenge_handler(bot, message, user_id, username)
        return
    elif text == handler_button_new_question or '✉️ Задать вопрос':
        await client_newquestion(message)

    photo_path = None
    caption = None
    reply_markup = None

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Telegram", url="https://t.me/DewinDevlog"),
        InlineKeyboardButton("Vkontakte", url="https://vk.com/dewinbot"),
        InlineKeyboardButton("Сайт", url="https://dewinbot.ru")
    )

    keyboard1 = InlineKeyboardMarkup()
    keyboard1.row(InlineKeyboardButton("Добавить бота в чат", url="https://t.me/dewinconferencebot?startgroup&admin=promote_members+delete_messages+restrict_members+invite_users+pin_messages+manage_video_chats"))
    keyboard1.row(InlineKeyboardButton("Инструкция", url="https://dewinbot.ru/invite"), InlineKeyboardButton("Видео-гайд", url="https://dewinbot.ru/sorry"))

    keyboard2 = InlineKeyboardMarkup()
    keyboard2.add(InlineKeyboardButton("🔗 Список всех команд бота", url="https://dewinbot.ru/commands"))

    keyboard3 = InlineKeyboardMarkup()
    keyboard3.add(InlineKeyboardButton("🛠 Тех. поддержка", callback_data="tech_support"))

    # Изменения здесь: обращаемся к ключам словарей
    if text == "🛡 Добавить бота в чат":
        photo_path, caption = invite["🛡 Добавить бота в чат"]
        reply_markup = keyboard1
    elif text == "📁 О проекте":
        photo_path, caption = project["📁 О проекте"]
        reply_markup = keyboard
    elif text == "🔗 Команды":
        photo_path, caption = commands["🔗 Команды"]
        reply_markup = keyboard2
    elif text == "🛠 Тех. поддержка":
        photo_path, caption = tex["🛠 Тех. поддержка"]
        reply_markup = keyboard3

    if photo_path and os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            await bot.send_photo(chat_id=user_id, photo=photo, caption=caption, parse_mode="HTML", reply_markup=reply_markup)
    elif caption: 
        await bot.send_message(user_id, caption, reply_markup=reply_markup, parse_mode="HTML")
    else: 
        # Можно добавить дефолтный ответ или просто ничего не делать
        pass