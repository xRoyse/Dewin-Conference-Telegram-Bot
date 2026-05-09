import asyncio
import os
import logging
from datetime import datetime

from database.database import create_banned_table, create_marriages_table, create_muted_table, create_groups_table, \
    create_users_table, create_memberships_table, check_and_update_group_title, create_achievements_table, \
    create_user_achievement_progress_table, create_user_achievements_table, insert_achievements
from database.export import start_scheduler
from utils.achievement_manager import AchievementsManager
from utils.loader import dp, bot
from aiogram import types
from aiogram.utils import executor

from commands.admins.handlers import *
from commands.entertaining.events.handlers import *
from commands.entertaining.wedding.handlers import *
from commands.entertaining.interactions.handlers import *
from commands.notifications.handlers import *
from commands.public.handlers import *
from commands.private.handlers import *
from commands.developers.handlers import *
from support.handlers import client, admin, fsm


async def on_startup(dispatcher):
    await create_groups_table()
    await create_users_table()
    await create_memberships_table()
    await create_marriages_table()
    await create_muted_table()
    await create_banned_table()
    await create_achievements_table()
    await create_user_achievement_progress_table()
    await create_user_achievements_table()
    await insert_achievements()
    start_scheduler()
    asyncio.create_task(check_muted_users(bot))
    asyncio.create_task(check_unban(bot))
    client.register_handler_client(dp)
    admin.register_handler_admin(dp)
    fsm.register_handler_FSM(dp)


@dp.message_handler(lambda message: message.chat.type in ['group', 'supergroup'] and not message.text.startswith(
    '/') and message.reply_to_message is None)
async def track_user_activity(message: types.Message):
    group_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or "No username" 
    admin_level = 0
    data_reg = datetime.now().strftime('%H:%M %d-%m-%Y')

    # Апдейти тайтл
    await check_and_update_group_title(group_id, message.chat.title)
    await add_user_record(user_id, username)
    user_added = await add_membership_record(group_id, user_id, admin_level, data_reg=data_reg)
    await add_message(group_id, user_id, username)

    # Передаем username в функцию add_message
    await add_message(group_id, user_id, username=username)

    await AchievementsManager.track_progression(
        user_id,
        base_code="msgs",
        thresholds=[1000, 5000, 10000, 25000],
        metadata={"increment": 1}
    )
    # Для любых других достижений используем
    await AchievementsManager.handle_event(user_id, code="1000_msgs", metadata={"increment": 1})


    if user_added:
        await bot.send_message(
            dew_channel,
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> добавлен в БД</b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
            parse_mode="HTML", message_thread_id=log_message_thread_id
        )

    # Вызываем message_handler для всех сообщений, прошедших фильтры
    await message_handler(bot, message)


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    if not os.path.exists("media"):
        print("Папка 'media' не найдена.")
    elif not os.path.exists("media/gif"):
        print("Папка 'gif' не найдена.")
    elif not os.path.exists("media/photos"):
        print("Папка 'photos' не найдена.")
    elif not os.path.exists("media/videos"):
        print("Папка 'videos' не найдена.")
    else:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
