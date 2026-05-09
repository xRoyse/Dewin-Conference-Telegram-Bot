from aiogram import types
from config import bot

from ..wedding.wedding import *
from ..wedding.divorces import *
from ..wedding.marriage import *

from utils.loader import dp

@dp.message_handler(commands=['wedding'])
async def wedding_command(message: types.Message):
    await wedding_message_handler(message)

@dp.callback_query_handler(lambda c: c.data.startswith('wedding_accept'))
async def accept_wedding_callback(callback: types.CallbackQuery):
    _, user1_id, user2_id, group_id = callback.data.split(":")
    await accept_wedding(callback, int(user1_id), int(user2_id), int(group_id))

@dp.callback_query_handler(lambda c: c.data.startswith('wedding_decline'))
async def decline_wedding_callback(callback: types.CallbackQuery):
    _, user2_id = callback.data.split(":")
    await decline_wedding(callback, int(user2_id))
    
@dp.message_handler(commands=['marriage'])
async def marriage_command(message: types.Message):
    await marriage_message_handler(bot, message)

@dp.message_handler(commands=['divorce'])
async def divorce_command(message: types.Message):
    await divorce_messege_handler(message)

@dp.callback_query_handler(lambda c: c.data.startswith('divorce_confirm'))
async def divorce_confirm_callback(callback: types.CallbackQuery):
    _, marriage_id, group_id = callback.data.split(":")
    await accept_divorce(callback, int(marriage_id), int(group_id))

@dp.callback_query_handler(lambda c: c.data == 'divorce_cancel')
async def divorce_cancel_callback(callback: types.CallbackQuery):
    await cancel_divorce(callback)