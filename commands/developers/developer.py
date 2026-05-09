from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command


from config import DEVELOPER
from database.database import create_table, async_session
from sqlalchemy import text
from datetime import datetime


async def cmd_add_admin(message: types.Message):
    """Команда повышения себя до администратора с уровнем 5 в группе."""
    if message.from_user.id == DEVELOPER:
        group_id = message.chat.id
        user_id = message.from_user.id
        username = message.from_user.username or f"user{user_id}"
        data_reg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            async with async_session() as session:
                # Вставка или апдейт записи с admin_level = 5
                result = await session.execute(
                    text(f"""SELECT 1 FROM "tgr_{group_id}" WHERE user_id = :user_id"""),
                    {"user_id": user_id}
                )
                if result.scalar():
                    # Запись уже существуют — просто апдейтим
                    await session.execute(
                        text(f"""UPDATE "tgr_{group_id}" SET admin_level = 5 WHERE user_id = :user_id"""),
                        {"user_id": user_id}
                    )
                else:
                    # В противном случае вставляем с admin_level = 5
                    await session.execute(
                        text(f"""INSERT INTO "tgr_{group_id}" (user_id, username, admin_level, data_reg, sms, exp, reputation)
                                   VALUES (:user_id, :username, 5, :data_reg, 0, 0, 0)"""),
                        {"user_id": user_id, "username": username, "data_reg": data_reg}
                    )

                await session.commit()

                await message.answer(f"<b>Выданы права разработчика в группе <code>{message.chat.title}</code>!</b>", parse_mode='HTML')
        except Exception as e:
            await message.answer(f"❌ Ошибка: {e}")

    else:
        await message.answer("<b>Эй... Не балуйся командой! Маленький ещё 😉</b>", parse_mode='HTML')
