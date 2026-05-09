from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import cfg

mainmenunewsupport = KeyboardButton(cfg['button_new_question'])
mainback = KeyboardButton(cfg['button_back'])
mainmenu = ReplyKeyboardMarkup(resize_keyboard=True).row(mainmenunewsupport, mainback)