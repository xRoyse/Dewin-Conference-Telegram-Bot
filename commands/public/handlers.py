from aiogram import types

from config import bot
from utils.loader import dp

from .reg import *
from .admins import *
from .help import *
from .quit import *
from .top import *
from .profile import *
from .info import *
from .weather import *
from .translate import *
from .group import *
from .links import *
from .mems import *

@dp.message_handler(commands=['reg'])
async def reg_command(message: types.Message):
    await reg_command_handler(bot, message)
    
@dp.message_handler(commands=['admins', "админс", "админы"], commands_prefix='!?./')
async def admins_command(message: types.Message):
    await admins_command_handler(bot, message)
    
@dp.message_handler(commands=['help', "хепл", "помощь"], commands_prefix='!?./')
async def help_command(message):
    await help_command_hendler(bot, message) 

@dp.message_handler(commands=["q", "выйти"], commands_prefix='!?./')
async def q_command(message: types.Message):
    await q_command_handler(message)

@dp.message_handler(commands=["quit"], commands_prefix='!?./')
async def q_command(message: types.Message):
    await q_command_handler(message)

@dp.callback_query_handler(confirm_leave_cb.filter(action="confirm"))
async def handle_confirm_leave_callback(query: types.CallbackQuery, callback_data: dict):
    await confirm_leave_callback(query, callback_data)

@dp.callback_query_handler(confirm_leave_cb.filter(action="cancel"))
async def handle_cancel_leave_callback(query: types.CallbackQuery, callback_data: dict):
    await cancel_leave_callback(query, callback_data)
    
@dp.message_handler(commands=['top', "топ"], commands_prefix='!?./')
async def top_command(message: types.Message):
    await top_command_handler(bot, message)

@dp.message_handler(commands=['profile', "профиль"], commands_prefix='!?./')
async def profile_command(message: types.Message):
    await profile_command_handler(bot, message)

@dp.callback_query_handler(lambda c: c.data.startswith('marriage_info'))
async def marriage_info(callback: types.CallbackQuery):
    _, user_id, group_id = callback.data.split(":")
    user_id, group_id = int(user_id), int(group_id)
    await marriage_info_callback(callback, user_id, group_id)
    
@dp.message_handler(commands=['info', "инфо"], commands_prefix='!?./')
async def info_command(message: types.Message):
    await info_command_handler(bot, message)

@dp.message_handler(commands=['weather', "погода"], commands_prefix='!?./')
async def weather_command(message: types.Message):
    await weather_command_handler(message)

@dp.message_handler(commands=['translate', 'перевести'], commands_prefix='!?./')
async def translate_command(message: types.Message):
    await translate_command_handler(message)

@dp.callback_query_handler(translate_cb.filter())
async def translate_callback(query: types.CallbackQuery, callback_data: dict):
    await translate_callback_handler(query, callback_data)

@dp.message_handler(commands=['group', 'группа'], commands_prefix='!?./')
async def group_command(message: types.Message):
    await group_command_handler(bot, message)

@dp.message_handler(commands=['groupusers', 'группапользователи'], commands_prefix='!?./')
async def group_users_command(message: types.Message):
    await group_users_command_handler(bot, message)

@dp.message_handler(commands=['links', 'ссылка', 'сократи', 'дштлы', 'ccskrf'], commands_prefix='!?/')
async def shorten_link(message: types.Message):
    await shorten_link_command(bot, message)

@dp.message_handler(commands=['mems', 'мемы', 'мем'], commands_prefix='!?./')
async def mems_command(message: types.Message):
    await mems_command_handler(message)