from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.loader import dew_channel, log_message_thread_id

async def send_ehelp(bot, message: types.Message):
    help_text = (
        f"<b>Список развлекательных команд:</b>\n"
        f"<blockquote><b>·</b> /hug - обнять\n"
        f"<b>·</b> /love - заняться любовью\n"
        f"<b>·</b> /hit - ударить\n"
        f"<b>·</b> /kiss - поцеловать\n"
        f"<b>·</b> /slap - дать пощечину\n"
        f"<b>·</b> /dance - пригласить на танец\n"
        f"<b>·</b> /highfive - дать пять\n"
        f"<b>·</b> /boop - легонько ударить по носу\n"
        f"<b>·</b> /headpat - погладить по голове\n"
        f"<b>·</b> /compliment - сделать комплимент\n"
        f"<b>·</b> /wave - помахать рукой\n"
        f"<b>·</b> /wishluck - пожелать удачи\n"
        f"<b>·</b> /handshake - рукопожатие\n"
        f"<b>·</b> /good_morning - пожелать доброго утра\n"
        f"<b>·</b> /good_night - пожелать доброй ночи</blockquote>\n\n"
        f"<b>Список свадебных команд</b>\n"
        f"<blockquote><b>·</b>/wedding - Пожениться\n"
        f"<b>·</b>/divorce - Развестись\n"
        f"<b>·</b>/marriage - Список браков в группе\n</blockquote>"
        )
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔗 Список всех команд бота", url="https://dewinbot.ru/commands"))
    
    await message.reply(help_text, reply_markup=keyboard, parse_mode="HTML")
    await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/ehelp</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
            parse_mode="HTML", 
            message_thread_id=log_message_thread_id
            )
    