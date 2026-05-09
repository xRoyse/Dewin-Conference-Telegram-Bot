from commands.entertaining.interactions.ehelp import *
from commands.entertaining.interactions.hug import *
from commands.entertaining.interactions.kiss import *
from commands.entertaining.interactions.love import *
from commands.entertaining.interactions.dance import *
from commands.entertaining.interactions.highfive import *
from commands.entertaining.interactions.handshake import *
from commands.entertaining.interactions.hit import *
from commands.entertaining.interactions.boop import *
from commands.entertaining.interactions.headpat import *
from commands.entertaining.interactions.compliment import *
from commands.entertaining.interactions.wave import *
from commands.entertaining.interactions.slap import *
from commands.entertaining.interactions.wishluck import *
from commands.entertaining.interactions.good_morning import *
from commands.entertaining.interactions.good_night import *

from commands.admins.ahelp import *
from commands.admins.all import *
from commands.admins.delladmin import *
from commands.admins.setadmin import *
from commands.admins.sms import *
from commands.admins.ban import *
from commands.admins.unban import *
from commands.admins.mute import *
from commands.admins.unmute import *

from commands.public.admins import *
from commands.public.help import *
from commands.public.profile import *
from commands.public.info import *
from commands.public.quit import *
from commands.public.reg import *
from commands.public.top import *

"""
[*] На переделку!
"""
async def handlers_commands(bot, message: types.Message):
        text = message.text
        
        if text == "/boop" or text == '.boop' or text == '!boop' or text == '?boop':
            await boop_command_handler(message)
            return
        elif text == "/compliment" or text == '.compliment' or text == '!compliment' or text == '?compliment' or text == '/комплимент' or text == '.комплимент' or text == '!комплимент' or text == '?комплимент':
            await compliment_command_handler(message)
            return
        elif text == "/dance" or text == '.dance' or text == '!dance' or text == '?dance' or text == '/танец' or text == 'танец' or text == '!танец' or text == '?танец':
                await dance_command_handler(message)
                return
        elif text == "/good_morning" or text == '.good_morning' or text == '!good_morning' or text == '?good_morning' or text == '/доброе_утро' or text == '.доброе_утро' or text == '!доброе_утро' or text == '?доброе_утро':
                await good_morning_command_handler(message)
                return
        elif text == "/good_night" or text == '.good_night' or text == '!good_night' or text == '?good_night' or text == '/доброй_ночи' or text == '.доброй_ночи' or text == '!доброй_ночи' or text == '?доброй_ночи':
                await good_night_command_handler(message)
                return
        elif text == "/headpat" or text == '.headpat' or text == '!headpat' or text == '?headpat':
                await headpat_command_handler(message)
                return
        elif text == "/highfive" or text == '.highfive' or text == '!highfive' or text == '?highfive' or text == '/дать_пять' or text == '.дать_пять' or text == '!дать_пять' or text == '?дать_пять':
                await highfive_command_handler(message)
                return
        elif text == "/hit" or text == '.hit' or text == '!hit' or text == '?hit' or text == '/ударить' or text == '.ударить' or text == '!ударить' or text == '?ударить':
                await hit_command_handler(message)
                return
        elif text == "/hug" or text == '.hug' or text == '!hug' or text == '?hug' or text == '/обнять' or text == '.обнять' or text == '!обнять' or text == '?обнять':
                await hug_command_handler(message)
                return
        elif text == "/kiss" or text == '.kiss' or text == '!kiss' or text == '?kiss' or text == '/поцеловать' or text == '.поцеловать' or text == '!поцеловать' or text == '?поцеловать':
                await kiss_command_handler(message)
                return
        elif text == "/love" or text == '.love' or text == '!love' or text == '?love' or text == '/любить' or text == '.любить' or text == '!любить' or text == '?любить':
                await love_command_handler(message)
                return
        elif text == "/slap" or text == '.slap' or text == '!slap' or text == '?slap' or text == '/slap' or text == '.пощечина' or text == '!пощечина' or text == '?пощечина':
                await slap_command_handler(message)
                return
        elif text == "/wave" or text == '.wave' or text == '!wave' or text == '?wave' or text == '/помахать' or text == '.помахать' or text == '!помахать' or text == '?помахать':
                await wave_command_handler(message)
                return
        elif text == "/wishluck" or text == '.wishluck' or text == '!wishluck' or text == '?wishluck' or text == '/удачи' or text == '.удачи' or text == '!удачи' or text == '?удачи':
                await wishluck_command_handler(message)
                return
        elif text == "/handshake" or text == '.handshake' or text == '!handshake' or text == '?handshake' or text == '/рукопожатие' or text == '.рукопожатие' or text == '!рукопожатие' or text == '?рукопожатие':
                await handshake_callback_handler(message)
                return  
        elif text == "/info" or text == "/info@DewinConferenceBot" or text == "/info@Dewin_Moder_Bot":
                await info_command_handler(bot, message)
                return
        elif text == "/admins" or text == "/admins@DewinConferenceBot" or text == "/admins@Dewin_Moder_Bot":
                await admins_command_handler(bot, message)
                return
        elif text == "/help" or text == "/help@DewinConferenceBot" or text == "/help@Dewin_Moder_Bot":
                await help_command_hendler(bot, message)
                return
        elif text == "/profile" or text == "/profile@DewinConferenceBot" or text == "/profile@Dewin_Moder_Bot":
                await profile_command_handler(bot, message)
                return
        elif text == "/quit" or text == "/quit@DewinConferenceBot" or text == "/quit@Dewin_Moder_Bot":
                await q_command_handler(bot, message)
                return
        elif text == "/q" or text == "/q@DewinConferenceBot" or text == "/q@Dewin_Moder_Bot":
                await q_command_handler(bot, message)
                return
        elif text == "/reg" or text == "/reg@DewinConferenceBot" or text == "/reg@Dewin_Moder_Bot":
                await reg_command_handler(bot, message)
                return
        elif text == "/top" or text == "/top@DewinConferenceBot" or text == "/top@Dewin_Moder_Bot":
                await top_command_handler(bot, message)
                return
        elif text == "/ahelp" or text == "/ahelp@DewinConferenceBot" or text == "/ahelp@Dewin_Moder_Bot":
                await admin_help_handlers(bot, message)
                return
        elif text == "/ehelp" or text == "/ehelp@DewinConferenceBot" or text == "/ehelp@Dewin_Moder_Bot":
                await send_ehelp(bot, message)
                return
        elif text == "/all" or text == "/all@DewinConferenceBot" or text == "/all@Dewin_Moder_Bot":
                await mention_all_members_handlers(bot, message)
                return
        elif text == "/delladmin" or text == "/delladmin@DewinConferenceBot" or text == "/delladmin@Dewin_Moder_Bot":
                await delladmin_handlers(bot, message)
                return
        elif text == "/setadmin" or text == "/setadmin@DewinConferenceBot" or text == "/setadmin@Dewin_Moder_Bot":
                await settadmin_handlers(bot, message)
                return
        elif text == "/sms" or text == "/sms@DewinConferenceBot" or text == "/sms@Dewin_Moder_Bot":
                await send_mention_message_handlers(bot, message)
                return
        elif text == "/mute" or text == '.mute' or text == '!mute' or text == '?mute' or text == '/мут' or text == '.мут' or text == '!мут' or text == '?мут':
                await mute_handlers(bot, message)
                return
        elif text == "/unmute" or text == '.unmute' or text == '!unmute' or text == '?unmute' or text == '/унмут' or text == '.унмут' or text == '!унмут' or text == '?унмут':
                await unmute_handlers(bot, message)
                return