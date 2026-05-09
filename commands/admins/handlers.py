from aiogram import types

from config import bot
from utils.loader import dp

from commands.admins.ahelp import *
from commands.admins.all import *
from commands.admins.setadmin import *
from commands.admins.delladmin import *
from commands.admins.sms import *
from commands.admins.ban import *
from commands.admins.unban import *
from commands.admins.banlist import *
from commands.admins.mute import *
from commands.admins.unmute import *
from commands.admins.mutelist import *
from commands.admins.kick import *

@dp.message_handler(commands=['ahelp', 'ахелп'], commands_prefix='!?./')
async def admin_help(message: types.Message):
    await admin_help_handlers(bot, message)

@dp.message_handler(commands=['all', 'алл', 'элл'], commands_prefix='!?./')
async def mention_all_members(message: types.Message):
    await mention_all_members_handlers(bot, message)
    
@dp.message_handler(commands=['setadmin', 'сетадмин'], commands_prefix='!?./')
async def settadmin(message: types.Message):
    if len(message.text.split()) < 2:
        await message.reply(
            "<b>Неверный формат команды</b>\n"
            "<blockquote><b>Используйте:</b><code> /setadmin «@тег» (ранг)</code></blockquote>",
            parse_mode='HTML'
        )
        return
    
    await settadmin_handlers(bot, message)
    
@dp.message_handler(commands=['delladmin', 'делладмин'], commands_prefix='!?./')
async def delladmin(message: types.Message):
    if len(message.text.split()) < 2:
        await message.reply(
            "<b>Неверный формат команды</b>\n"
            "<blockquote><b>Используйте:</b><code> /delladmin «@тег» (ранг)</code></blockquote>",
            parse_mode='HTML'
        )
        return
    
    await delladmin_handlers(bot, message)
    
@dp.message_handler(commands=['sms', 'смс', 'сообщение', 'увед'], commands_prefix='!?./')
async def sms_handler(message: types.Message):
    await send_mention_message_handlers(message, bot)

@dp.callback_query_handler(lambda call: call.data.startswith("confirm_send_empty"))
async def handle_confirm_empty(call: types.CallbackQuery):
    await process_confirm_send_empty(call, bot)

@dp.callback_query_handler(lambda call: call.data == "cancel_send")
async def handle_cancel_send(call: types.CallbackQuery):
    await cancel_send(call)
    
@dp.message_handler(commands=['мут', 'mute', 'ьгеу', 'ven'], commands_prefix='!?./')
async def mute(message: types.Message):
    await mute_handlers(bot, message)

@dp.message_handler(commands=['унмут', 'unmute', 'гтьгеу', 'eyven'], commands_prefix='!?./')
async def unmute(message: types.Message):
    await unmute_handlers(bot, message)

@dp.message_handler(commands=['мутлист', 'mutelist', 'ьгеудшые', 'venkbcn', 'млист', 'mlist', 'ьдшые', 'vkbcn'], commands_prefix='!?./')
async def mutelist(message: types.Message):
    await mutelist_handler(bot, message)

# Обработчик команды /ban
@dp.message_handler(commands=['бан', 'ban', 'ифт', ',fy'], commands_prefix='!?./')
async def ban(message: types.Message):
    await ban_handlers(bot, message)
    
@dp.message_handler(commands=['унбан', 'unban', 'гтифт', 'ey,fy', 'разбан'], commands_prefix='!?./')
async def unban(message: types.Message):
    await unban_handlers(bot, message)

@dp.message_handler(commands=['банлист', 'banlist', 'ифтдшые', ',fykbcn', 'блист', 'blist', 'идшые', ',kbcn'], commands_prefix='!?./')
async def banlist(message: types.Message):
    await banlist_handler(bot, message)

@dp.message_handler(commands=['кик', 'kick', 'лшсл', 'rbr'], commands_prefix='!?./')
async def kick(message: types.Message):
    await kick_handler(bot, message)
