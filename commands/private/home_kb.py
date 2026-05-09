import os
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def home_handler(message):
    user_id = message.from_user.id
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
    await message.bot.send_message(user_id, "Вы были перенаправлены на главное меню!", reply_markup=keyboard)