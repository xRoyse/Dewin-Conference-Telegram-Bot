from aiogram import types
from config import bot

from .convent_db import *
from .post import *
from .developer import *

from utils.loader import dp

@dp.message_handler(commands=['db'])
async def db_command(message: types.Message):
    output_file_path = "database.txt"
    await convert_db_to_txt(output_file_path)
    await bot.send_document(message.chat.id, open(output_file_path, 'rb'))
    
@dp.message_handler(commands=['mute_users'])
async def mute_users_command(message: types.Message):
    output_file_path = "muted_users.txt"
    await convert_mute_users_to_txt(output_file_path)
    await bot.send_document(message.chat.id, open(output_file_path, 'rb'))

@dp.message_handler(commands=['ban_users'])
async def ban_users_command(message: types.Message):
    output_file_path = "ban_users.txt"
    await convert_ban_users_to_txt(output_file_path)
    await bot.send_document(message.chat.id, open(output_file_path, 'rb'))

@dp.message_handler(commands=['list'])
async def marriage_command(message: types.Message):
    output_file_path = "marriage.txt"
    await convert_marriages_to_txt(output_file_path)
    await bot.send_document(message.chat.id, open(output_file_path, 'rb'))

@dp.message_handler(commands=['post12'])
async def handle_send_web_message(message: types.Message):
    await send_post_message(bot)
    await message.reply("Сообщение с фото отправлено в канал.")
    
@dp.message_handler(commands=['developer'])
async def cmd_developer(message: types.Message):
    await cmd_add_admin(message)
