from aiogram import types
from config import bot

from utils.loader import dp
from commands.private.keyboards import *
from commands.private.start import private_welcome_messenge_handler

@dp.message_handler(lambda message: message.chat.type == "private")
async def private_message(message: types.Message):
    await private_message_handler(bot, message)
    
@dp.message_handler(commands=['start'], chat_type=types.ChatType.PRIVATE)
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    await private_welcome_messenge_handler(bot, message, user_id, username)

@dp.callback_query_handler(lambda c: c.data == "tech_support")
async def tech_support_callback(callback_query: types.CallbackQuery):
    await client_start(callback_query.message)
