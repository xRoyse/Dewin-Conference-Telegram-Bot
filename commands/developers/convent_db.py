from aiogram import types
from sqlalchemy import text

from config import DEVELOPER
from database.database import async_session


async def convert_db_to_txt(message: types.Message, file_path: str) -> None:
    """
    Экспортирует содержимое таблицы memberships (с join к users) в текстовый файл,
    сгруппированное по group_id.
    """
    if message.from_user.id == DEVELOPER:
        async with async_session() as session:
            try:
                result = await session.execute(
                    text("""
                        SELECT 
                            m.group_id,
                            u.user_id,
                            u.username,
                            m.admin_level,
                            m.data_reg,
                            m.sms,
                            m.exp,
                            m.reputation
                        FROM memberships m
                        JOIN users u ON u.user_id = m.user_id
                        ORDER BY m.group_id, m.sms DESC
                    """)
                )
                rows = result.mappings().all()

                if not rows:
                    print("Нет данных для экспорта.")
                    return

                with open(file_path, 'w', encoding='utf-8') as f:
                    current_group = None
                    for row in rows:
                        if row['group_id'] != current_group:
                            current_group = row['group_id']
                            f.write(f"\nТаблица: group_{current_group}\n")
                            f.write("user_id | username | admin_level | data_reg | sms | exp | reputation\n")
                            f.write("-" * 80 + "\n")
                        f.write(
                            f"{row['user_id']} | {row['username'] or '—'} | {row['admin_level']} | {row['data_reg']} | {row['sms']} | {row['exp']} | {row['reputation']}\n")

                print(f"✅ База данных успешно экспортирована в {file_path}")

            except Exception as e:
                print(f"❌ Ошибка при экспорте: {e}")
    else:
        await message.answer("<b>Эй... Не балуйся командой! Маленький ещё 😉</b>", parse_mode='HTML')
        
async def convert_mute_users_to_txt(message: types.Message, file_path: str) -> None:
    """
    Конвертирует таблицу muted_users в текстовый файл.
    """
    if message.from_user.id == DEVELOPER:
        async with async_session() as session:
            query = "SELECT * FROM muted_users;"
            result = await session.execute(text(query))
            rows = result.fetchall()

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("Таблица: muted_users\n")
                f.write("user_id | username | group_id | group_name | until_date | comment\n")
                f.write("-" * 50 + "\n")

                for row in rows:
                    f.write(f"{row.user_id} | {row.username} | {row.group_id} | {row.group_name} | {row.until_date} | {row.comment}\n")
                f.write("\n")
                print(f"Данные из таблицы muted_users успешно конвертированы в {file_path}.")
    else:
        await message.answer("<b>Эй... Не балуйся командой! Маленький ещё 😉</b>", parse_mode='HTML')

async def convert_ban_users_to_txt(message: types.Message, file_path: str) -> None:
    """
    Конвертирует таблицу ban_users в текстовый файл.
    """
    if message.from_user.id == DEVELOPER:
        async with async_session() as session:
            query = "SELECT * FROM ban_users;"
            result = await session.execute(text(query))
            rows = result.fetchall()

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("Таблица: ban_users\n")
                f.write("user_id | username | group_id | group_name | until_date | reason\n")
                f.write("-" * 50 + "\n")

                for row in rows:
                    f.write(f"{row.user_id} | {row.username} | {row.group_id} | {row.group_name} | {row.until_date} | {row.reason}\n")
                f.write("\n")
                print(f"Данные из таблицы ban_users успешно конвертированы в {file_path}.")
    else:
        await message.answer("<b>Эй... Не балуйся командой! Маленький ещё 😉</b>", parse_mode='HTML')
        
async def convert_marriages_to_txt(message: types.Message, file_path: str) -> None:
    """
    Конвертирует таблицу marriages в текстовый файл.

    Аргументы:
        file_path (str): Путь к файлу, куда сохранить данные.
    """
    if message.from_user.id == DEVELOPER:
        async with async_session() as session:
            query = "SELECT * FROM marriages;"
            result = await session.execute(text(query))
            rows = result.fetchall()

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("📜 Список браков\n")
                f.write("=" * 50 + "\n")
                f.write("marriage_id | user1_id | user2_id | group_id | date_of_marriage\n")
                f.write("-" * 50 + "\n")

                for row in rows:
                    f.write(f"{row.marriage_id} | {row.user1_id} | {row.user2_id} | {row.group_id} | {row.date_of_marriage}\n")
                print(f"📂 Список браков сохранен в {file_path}.")
    else:
        await message.answer("<b>Эй... Не балуйся командой! Маленький ещё 😉</b>", parse_mode='HTML')