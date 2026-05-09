import os
import random
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import GIF_LOVE

async def love_command_handler(message: types.Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("<b>Эта команда должна быть ответом на сообщение пользователя.</b>", parse_mode='HTML')
        return

    target_user = message.reply_to_message.from_user
    initiator_user = message.from_user

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Согласиться", callback_data=f"love_accept_{target_user.id}_{initiator_user.id}"),
        InlineKeyboardButton("Отказаться", callback_data=f"love_decline_{target_user.id}_{initiator_user.id}")
    )

    await message.answer(
        f"<b>{target_user.get_mention(as_html=True)}, согласны ли вы заняться любовью с {initiator_user.get_mention(as_html=True)}?</b>",
        parse_mode="HTML",
        reply_markup=keyboard
    )

async def love_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    action, target_id, initiator_id = data[1], int(data[2]), int(data[3])

    if callback_query.from_user.id != target_id:
        await callback_query.answer("Только пользователь, которому предложили заняться любовью, может нажать эту кнопку.", show_alert=True)
        return

    initiator_user = await callback_query.bot.get_chat(initiator_id)
    target_user = await callback_query.bot.get_chat(target_id)

    if action == 'accept':
        initiator_id = int(initiator_id)
        target_id = int(target_id)

        gifs = os.listdir(GIF_LOVE)
        gif_path = os.path.join(GIF_LOVE, random.choice(gifs))

        messages = [
            f"<b>{initiator_user.get_mention(as_html=True)} занялся(ась) любовью без обязательств вместе с {target_user.get_mention(as_html=True)}</b>",
            f"<b>{initiator_user.get_mention(as_html=True)} занялся(ась) любовью с {target_user.get_mention(as_html=True)}</b>",
            f"<b>{initiator_user.get_mention(as_html=True)} с трепетом и нежностью разделил(а) моменты абсолютной близости с {target_user.get_mention(as_html=True)}</b>"
        ]
        text = random.choice(messages)

        await callback_query.message.answer_document(open(gif_path, 'rb'), caption=text, parse_mode="HTML")
        
    elif action == 'decline':
        await callback_query.message.answer(
            f"<b>{target_user.get_mention(as_html=True)} отклонил(а) предложение {initiator_user.get_mention(as_html=True)} о любви.</b>",
            parse_mode="HTML"
        )
 
    await callback_query.message.delete()
    await callback_query.answer()