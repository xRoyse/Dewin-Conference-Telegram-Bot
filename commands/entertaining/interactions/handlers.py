import logging

from aiogram import types

from config import bot
from utils.loader import dp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from commands.entertaining.interactions.ehelp import *
from commands.entertaining.interactions.hug import *
from commands.entertaining.interactions.kiss import *
from commands.entertaining.interactions.love import *
from commands.entertaining.interactions.dance import *
from commands.entertaining.interactions.highfive import *
from commands.entertaining.interactions.handshake import *
from commands.entertaining.interactions.hit import *
from commands.entertaining.interactions.boop import *
from commands.entertaining.interactions.headpat import *
from commands.entertaining.interactions.compliment import *
from commands.entertaining.interactions.wave import *
from commands.entertaining.interactions.slap import *
from commands.entertaining.interactions.wishluck import *
from commands.entertaining.interactions.good_morning import *
from commands.entertaining.interactions.good_night import *

'''
Все команды повторно прописаны в условном операторе: ..event/reputation.py
Да не правильно, но я хз как это пофиксить
'''

@dp.message_handler(commands=['ehelp'], commands_prefix='!?./')
async def handle_ehelp(message):
    try:
        await send_ehelp(bot, message)
    except Exception as e:
        logger.error(f"Ошибка в обработчике /ehelp: {str(e)}")

@dp.message_handler(commands=["hug"], commands_prefix='!?./')
async def hug_command(message: types.Message):
    try:
        await hug_command_handler(message)
    except Exception as e:
        logger.error(f"Ошибка в обработчике /hug: {str(e)}")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("hug_"))
async def hug_callback(callback_query: types.CallbackQuery):
    try:
        await hug_callback_handler(callback_query)
    except Exception as e:
        logger.error(f"Ошибка в обработчике hug_callback: {str(e)}")

@dp.message_handler(commands=["kiss"])
async def kiss_command(message: types.Message):
    try:
        await kiss_command_handler(message)
    except Exception as e:
        logger.error(f"Ошибка в обработчике /kiss: {str(e)}")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("kiss_"))
async def kiss_callback(callback_query: types.CallbackQuery):
    try:
        await kiss_callback_handler(callback_query)
    except Exception as e:
        logger.error(f"Ошибка в обработчике kiss_callback: {str(e)}")

@dp.message_handler(commands=["love"])
async def love_command(message: types.Message):
    try:
        await love_command_handler(message)
    except Exception as e:
        logger.error(f"Ошибка в обработчике /love: {str(e)}")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("love_"))
async def love_callback(callback_query: types.CallbackQuery):
    try:
        await love_callback_handler(callback_query)
    except Exception as e:
        logger.error(f"Ошибка в обработчике love_callback: {str(e)}")

@dp.message_handler(commands=["dance"])
async def dance_command(message: types.Message):
    try:
        await dance_command_handler(message)
    except Exception as e:
        logger.error(f"Ошибка в обработчике /dance: {str(e)}")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("dance_"))
async def dance_callback(callback_query: types.CallbackQuery):
    try:
        await dance_callback_handler(callback_query)
    except Exception as e:
        logger.error(f"Ошибка в обработчике dance_callback: {str(e)}")

@dp.message_handler(commands=["highfive"])
async def highfive_command(message: types.Message):
    try:
        await highfive_command_handler(message)
    except Exception as e:
        logger.error(f"Ошибка в обработчике /highfive: {str(e)}")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("highfive_"))
async def highfive_callback(callback_query: types.CallbackQuery):
    try:
        await highfive_callback_handler(callback_query)
    except Exception as e:
        logger.error(f"Ошибка в обработчике highfive_callback: {str(e)}")

@dp.message_handler(commands=["handshake"])
async def handshake_command(message: types.Message):
    try:
        await handshake_command_handler(message)
    except Exception as e:
        logger.error(f"Ошибка в обработчике /handshake: {str(e)}")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("handshake_"))
async def handshake_callback(callback_query: types.CallbackQuery):
    await handshake_callback_handler(callback_query)
    
@dp.message_handler(commands=["hit"])
async def hit_command(message: types.Message):
    await hit_command_handler(message)
    
@dp.message_handler(commands=["boop"])
async def boop_command(message: types.Message):
    await boop_command_handler(message)
    
@dp.message_handler(commands=["headpat"])
async def headpat_command(message: types.Message):
    await headpat_command_handler(message)
    
@dp.message_handler(commands=["compliment"])
async def compliment_command(message: types.Message):
    await compliment_command_handler(message)
    
@dp.message_handler(commands=["wave"])
async def wave_command(message: types.Message):
    await wave_command_handler(message)
    
@dp.message_handler(commands=["slap"])
async def slap_command(message: types.Message):
    await slap_command_handler(message)
    
@dp.message_handler(commands=["wishluck"])
async def wishluck_command(message: types.Message):
    await wishluck_command_handler(message)
    
@dp.message_handler(commands=["good_morning"])
async def good_morning_command(message: types.Message):
    await good_morning_command_handler(message)
    
@dp.message_handler(commands=["good_night"])
async def good_night_command(message: types.Message):
    await good_night_command_handler(message)