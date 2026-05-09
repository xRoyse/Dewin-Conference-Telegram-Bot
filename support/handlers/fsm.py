from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from support.bot import bot,dp
from config import cfg

question_sended = cfg['question_ur_question_sended_message']
devid = cfg['dev_id']
errormessage = cfg['error_message']

class FSMQuestion(StatesGroup):
    text = State()
    photo = State()

async def load_text(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text
        await FSMQuestion.next()
        await message.reply('Отправьте фото')
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

async def load_photo(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['photo'] = message.photo[-1].file_id
        await bot.send_photo(devid, data['photo'], caption=f"Вопрос от {message.from_user.id}: {data['text']}")
        await message.reply(question_sended, parse_mode='Markdown')
        await state.finish()
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

def register_handler_FSM(dp):
    dp.register_message_handler(load_text, state=FSMQuestion.text)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMQuestion.photo)