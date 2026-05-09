import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from utils.loader import bot  

from database.database import get_stat

"""
Каждый день в 00:00 бот отправляет пользователю (user_id) статистику бота и прикрепляет бекат БД
"""
async def send_database_file():
    user_id = 1302525645
    file_path = "database/db.sqlite3"  
    stats = await get_stat()
    group_count, user_count, sms_count = stats

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            await bot.send_document(
                user_id, file, caption=f"<b>Статистика бота на</b> <code>{datetime.now().strftime('%d-%m-%Y')}</code>\n\n🛡 » <b>Количество групп:</b> <code>{group_count} </code>\n🎙 » <b>Количество пользователей в БД:</b> <code>{user_count} </code>\n📨 » <b>Количество сообщений:</b> <code>{sms_count} </code>"
                , parse_mode='html')

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_database_file, CronTrigger(hour=0, minute=0))
    scheduler.start()
