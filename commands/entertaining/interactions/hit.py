import os
import random
from aiogram import types

from config import GIF_HIT

async def hit_command_handler(message: types.Message):
    if not message.reply_to_message:
        await message.reply("<b>Эта команда должна быть ответом на сообщение пользователя.</b>", parse_mode='HTML')
        return
    
    gifs = os.listdir(GIF_HIT)
    gif_path = os.path.join(GIF_HIT, random.choice(gifs))
   
    messages = [
        f"<b>{message.from_user.get_mention(as_html=True)} очень сильно и очень больно ударил(а) {message.reply_to_message.from_user.get_mention(as_html=True)}!</b>",
        f"<b>{message.from_user.get_mention(as_html=True)} нанес(ла) сокрушительный удар по {message.reply_to_message.from_user.get_mention(as_html=True)}!</b>",
        f"<b>{message.from_user.get_mention(as_html=True)} атакует {message.reply_to_message.from_user.get_mention(as_html=True)} с невероятной силой!</b>"
    ]
   
    text = random.choice(messages)

    await message.answer_document(open(gif_path, 'rb'), caption=text, parse_mode="HTML")