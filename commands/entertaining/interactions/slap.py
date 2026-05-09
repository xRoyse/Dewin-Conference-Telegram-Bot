import os
import random
from aiogram import types

from config import GIF_SLAP

async def slap_command_handler(message: types.Message):
    if not message.reply_to_message:
        await message.reply("<b>Эта команда должна быть ответом на сообщение пользователя.</b>", parse_mode='HTML')
        return
    
    gifs = os.listdir(GIF_SLAP)
    gif_path = os.path.join(GIF_SLAP, random.choice(gifs))
   
    messages = [
        f"<b>{message.from_user.get_mention(as_html=True)} со всего размаха дал(а) пощечину {message.reply_to_message.from_user.get_mention(as_html=True)}!</b>",
        f"<b>{message.from_user.get_mention(as_html=True)} нанес(ла) легкую пощечину {message.reply_to_message.from_user.get_mention(as_html=True)}!</b>"
    ]
   
    text = random.choice(messages)

    await message.answer_document(open(gif_path, 'rb'), caption=text, parse_mode="HTML")
