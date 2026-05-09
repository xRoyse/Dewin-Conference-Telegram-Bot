import os
import random
from aiogram import types

from config import GIF_COMPLIMENT

async def compliment_command_handler(message: types.Message):
    if not message.reply_to_message:
        await message.reply("<b>Эта команда должна быть ответом на сообщение пользователя.</b>", parse_mode='HTML')
        return
    
    gifs = os.listdir(GIF_COMPLIMENT)
    gif_path = os.path.join(GIF_COMPLIMENT, random.choice(gifs))
   
    messages = [
        f"<b>{message.from_user.get_mention(as_html=True)} смотрев на {message.reply_to_message.from_user.get_mention(as_html=True)} отвесил(а) комплимент</b>"
    ]
   
    text = random.choice(messages)

    await message.answer_document(open(gif_path, 'rb'), caption=text, parse_mode="HTML")