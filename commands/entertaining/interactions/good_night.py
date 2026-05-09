import os
import random
from aiogram import types

from config import GIF_GOOD_NIGHT

async def good_night_command_handler(message: types.Message):
    if not message.reply_to_message:
        await message.reply("<b>Эта команда должна быть ответом на сообщение пользователя.</b>", parse_mode='HTML')
        return
    
    gifs = os.listdir(GIF_GOOD_NIGHT)
    gif_path = os.path.join(GIF_GOOD_NIGHT, random.choice(gifs))
   
    messages = [
        f"<b>{message.from_user.get_mention(as_html=True)} пожелал(а) хороших снов {message.reply_to_message.from_user.get_mention(as_html=True)}</b>",
        f"<b>{message.from_user.get_mention(as_html=True)} пожелал(а) спокойной ночи {message.reply_to_message.from_user.get_mention(as_html=True)}</b>",
        f"<b>{message.from_user.get_mention(as_html=True)} пожелал(а) доброй ночи {message.reply_to_message.from_user.get_mention(as_html=True)}</b>"
    ]
   
    text = random.choice(messages)

    await message.answer_document(open(gif_path, 'rb'), caption=text, parse_mode="HTML")