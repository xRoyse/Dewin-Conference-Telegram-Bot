import os
import random
from aiogram import types

from config import GIF_BOOP

async def boop_command_handler(message: types.Message):
    if not message.reply_to_message:
        await message.reply("<b>Эта команда должна быть ответом на сообщение пользователя.</b>", parse_mode='HTML')
        return
    
    gifs = os.listdir(GIF_BOOP)
    gif_path = os.path.join(GIF_BOOP, random.choice(gifs))
   
    messages = [
        f"<b>{message.from_user.get_mention(as_html=True)} легко ударил(а) {message.reply_to_message.from_user.get_mention(as_html=True)} по носу</b>",
        f"<b>{message.from_user.get_mention(as_html=True)} игриво ударил(а) {message.reply_to_message.from_user.get_mention(as_html=True)} по носу</b>"
    ]
   
    text = random.choice(messages)

    await message.answer_document(open(gif_path, 'rb'), caption=text, parse_mode="HTML")