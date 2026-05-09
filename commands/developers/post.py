from aiogram import types
from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup

from config import DEVELOPER
from utils.loader import *

async def send_post_message(bot, message: types.Message):
    if message.from_user.id == DEVELOPER:
        keyboard = InlineKeyboardMarkup()
        url_button = InlineKeyboardButton(text="Добавить бота в группу 💙", url="https://vk.com/@dewinbot-update-1-2")
        keyboard.add(url_button)

        photo1 = InputFile("media/photos/Закреп.png") 

        await bot.send_photo(
            chat_id=channel_post,
            photo=photo1,
            caption=(
                    f"<b>Привет!\n\n"
                    f"Я <code>Dewin » ConferenceBot</code> и могу тебе помочь с возможностью модерирования группы, удобного информирования пользователей, а так же принесу вам в группу развлечения!\n\n"
                    f"Если стало инересно, добавляй бота к себе в группу! А дополнительную информацию можешь найти у нас на сайте или в ЛС бота</b>"),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    else:
        await message.answer("<b>Эй... Не балуйся командой! Маленький ещё 😉</b>", parse_mode='HTML')