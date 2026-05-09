from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import bot

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dew_channel = -1002183906407  
channel_post = '@DewinDevlog'

log_message_thread_id = 4
task_message_thread_id = 6
communication_message_thread_id = 3
idea_message_thread_id = 7


message_thread_id=log_message_thread_id