from aiogram import types

from database.database import add_user_record,add_membership_record, remove_membership_record

from ..notifications.entering import *

from config import bot
from utils.loader import dp

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome_new_member(message: types.Message):
    for user in message.new_chat_members:
        await send_group_welcome(bot, message, user, add_user_record,add_membership_record)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('unban_'))
async def unban_user(callback_query: types.CallbackQuery):
    await unban_user_handler(bot, callback_query.message, callback_query)

@dp.message_handler(content_types=["left_chat_member"])
async def left_member(message: types.Message):
    await send_left_member(bot, message, remove_membership_record)