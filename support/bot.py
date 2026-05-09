from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import *

storage = MemoryStorage()
bot = Bot(token=cfg['token'])
dp = Dispatcher(bot, storage=storage)