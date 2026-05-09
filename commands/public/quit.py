from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.loader import dew_channel, log_message_thread_id
from database.database import remove_membership_record

confirm_leave_cb = CallbackData("leave", "action", "user_id","group_id")

async def q_command_handler(bot, message: types.Message):
    user_id = message.from_user.id
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Подтвердить", callback_data=confirm_leave_cb.new(action="confirm", user_id=user_id,group_id=message.chat.id)),
        InlineKeyboardButton("Отменить", callback_data=confirm_leave_cb.new(action="cancel", user_id=user_id, group_id=message.chat.id))
    )

    await message.answer(
        "<b>Вы уверены, что хотите выйти из беседы?\nДля подтверждения действия нажмите на соответствующую клавишу</b>",
        reply_markup=keyboard, parse_mode="HTML")
    await bot.send_message(
        dew_channel, 
        f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
        f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> покинул группу используя команду <code>/q (/quit)</code></b>\n"
        f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
        parse_mode="HTML", message_thread_id=log_message_thread_id
    )
    
async def confirm_leave_callback(query: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data['user_id'])
    group_id = int(callback_data['group_id'])

    if query.from_user.id != user_id:
        await query.answer("<b>Вы не можете подтверждать это действие.</b>", show_alert=True, parse_mode="HTML")
        return

    await query.message.edit_text(f"<a href='tg://user?id={user_id}'>Пользователь</a> покинул беседу по собственному желанию", parse_mode="HTML")
    await remove_membership_record(group_id,user_id)
    await query.bot.kick_chat_member(chat_id=query.message.chat.id, user_id=user_id)

async def cancel_leave_callback(query: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data['user_id'])

    if query.from_user.id != user_id:
        await query.answer("<b>Вы не можете отменить это действие.</b>", show_alert=True, parse_mode="HTML")
        return

    await query.message.edit_text("<b>Действие отменено</b>", parse_mode="HTML")