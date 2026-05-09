from aiogram import types

from config import bot
from utils.loader import dp

from ..events.reputation import *

@dp.message_handler(lambda message: message.chat.type in ['group'] and message.reply_to_message is not None)
async def reputation_message(message: types.Message):
    await reputation_message_handler (bot, message)
    
