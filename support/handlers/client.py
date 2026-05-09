from aiogram import types
from aiogram.dispatcher import Dispatcher

from commands.private.home_kb import home_handler
import support.kb as kb
from support.bot import dp, bot
from support.handlers.fsm import FSMQuestion
from support.handlers.db import db_profile_exist, db_profile_insertone, db_profile_banned
from config import cfg
from utils.loader import *


welcomemessage = cfg['welcome_message']
errormessage = cfg['error_message']
devid = cfg['dev_id']
question_first_msg = cfg['question_type_ur_question_message']

handler_button_new_question = cfg['button_new_question']
handler_button_back = cfg['button_back']


async def client_start(message: types.Message):
    try:
        if(message.chat.type != 'private'):
            await message.answer('Данную команду можно использовать только в личных сообщениях с ботом.')
            return
        if db_profile_exist(message.from_user.id):
            await message.answer(f'{welcomemessage}',parse_mode='Markdown', reply_markup=kb.mainmenu)
        else:
            user_id = message.from_user.id
            db_profile_insertone({
                '_id': message.from_user.id,
                'username': message.from_user.username,
                'access': 0,
                'ban': 0
            })
            await bot.send_message(
                dew_channel,
                f"Новый пользователь в тех. поддержке -> <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>!\nID пользователя: <code>{user_id}</code>",
                parse_mode="HTML",
                message_thread_id=log_message_thread_id
            )
            await message.answer(f'{welcomemessage}',parse_mode='Markdown', reply_markup=kb.mainmenu)
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')


async def client_newquestion(message: types.Message):
    try:
        if message.text == handler_button_new_question:
            if db_profile_banned(message.from_user.id):
                await message.answer("⚠ Вы *заблокованы* в тех. поддержке!", parse_mode='Markdown')
                return
            await message.answer(f"{cfg['question_type_ur_question_message']}")
            await FSMQuestion.text.set()
        elif message.text == handler_button_back:
            await home_handler(message)

    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')


async def client_getgroupid(message: types.Message):
    try:
        await message.answer(f"Chat id is: *{message.chat.id}*\nYour id is: *{message.from_user.id}*", parse_mode='Markdown')
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(client_getgroupid, commands=['getchatid'])
    dp.register_message_handler(client_newquestion)