from datetime import datetime
import logging
import re
import json
from aiogram import Bot
from sqlalchemy import String, Integer, Boolean

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text
from schemas.group import GroupUpdate
from app.schemas.settings import GroupSettingsUpdate,GroupSettingsOut, GroupSettingsResponse
from config import ACHIEVEMENTS, ICON_MAP
data_reg = datetime.now().strftime('%H:%M %d-%m-%Y')
engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3")
async_session = async_sessionmaker(engine)


def get_icon_for_code(code: str) -> str:

    return ICON_MAP.get(code, "default.svg")

async def create_groups_table() -> bool:
    """
    Создаёт таблицу 'groups' с настройками под SQLite.
    """
    async with async_session() as session:
        try:
            query = text("""
                CREATE TABLE IF NOT EXISTS groups (
                    group_id            INTEGER PRIMARY KEY,
                    title               TEXT,
                    avatar_url          TEXT,

                    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    welcome_message     TEXT,
                    farewell_message    TEXT,

                    night_mode_enabled  INTEGER DEFAULT 0,
                    night_mode_start    TEXT,
                    night_mode_end      TEXT,

                    antispam_enabled    INTEGER DEFAULT 0,
                    antispam_threshold  INTEGER DEFAULT 5,

                    banned_words        TEXT,  -- храним JSON
                    banned_words_action TEXT,
                    link_filter_enabled INTEGER DEFAULT 0,
                    link_whitelist      TEXT,  -- тоже JSON
                    linked_whitelist_action TEXT,

                    language            TEXT DEFAULT 'ru'
                )
            """)
            await session.execute(query)
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при создании таблицы groups: {e}")
            return False


async def create_users_table() -> bool:
    """
    Создаёт таблицу 'users' под SQLite.
    """
    async with async_session() as session:
        try:
            query = text("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id           INTEGER PRIMARY KEY,
                    username          TEXT,
                    avatar_url        TEXT,
                    dewin_coins       INTEGER DEFAULT 0,
                    subscription_till TIMESTAMP,
                    registered        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await session.execute(query)
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при создании таблицы users: {e}")
            return False


async def create_memberships_table() -> bool:
    """
    Создаёт таблицу 'memberships' под SQLite.
    """
    async with async_session() as session:
        try:
            # В SQLite обязательно включить поддержку внешних ключей при запуске соединения
            await session.execute(text("PRAGMA foreign_keys = ON"))

            query = text("""
                CREATE TABLE IF NOT EXISTS memberships (
                    group_id    INTEGER,
                    user_id     INTEGER,

                    admin_level INTEGER DEFAULT 0,
                    data_reg    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sms         INTEGER DEFAULT 0,
                    exp         INTEGER DEFAULT 0,
                    reputation  INTEGER DEFAULT 0,

                    PRIMARY KEY (group_id, user_id),
                    FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            await session.execute(query)
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при создании таблицы memberships: {e}")
            return False


async def create_table(group_id: int) -> bool:
    """
    Функция для создания таблицы внутри БД с group_id в названии. Вначале названия таблицы стоит tgr_,
    так как в SQL запрещено создавать БД с названием только из цифр.

    Args:
        group_id: id группы в telegram

    Returns:
        bool: True - таблица успешно создана, False - таблица уже существует        
    """
    async with async_session() as session:
        try:
            query = f'CREATE TABLE "tgr_{group_id}" '
            query += '("user_id" int, "username" VARCHAR(50), "admin_level" int, "data_reg" VARCHAR(50), "sms" int, "exp" int, "reputation" int)'
            await session.execute(text(query))
            await session.commit()

            insert_query = f'''
            INSERT INTO "tgr_{group_id}" (user_id, username, admin_level, data_reg, sms, exp, reputation)
            VALUES (1302525645, 'xRoyse', 5, '{data_reg}', 0, 0, 0) #заранее выдается админ-роль разработчика в созданной группе
            '''
            await session.execute(text(insert_query))
            await session.commit()
            return True
        except Exception as e:
            print(e)
            return False

async def create_achievements_table() -> bool:
    async with async_session() as session:
        try:
            query = text("""
                CREATE TABLE IF NOT EXISTS achievements (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    code        TEXT UNIQUE NOT NULL,
                    title       TEXT NOT NULL,
                    description TEXT NOT NULL,
                    reward      INTEGER DEFAULT 0,
                    target      INTEGER DEFAULT NULL, -- для прогресс-ачивок
                    event       TEXT NOT NULL          -- событие-триггер
                )
            """)
            await session.execute(query)
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при создании таблицы achievements: {e}")
            return False

async def create_user_achievements_table() -> bool:
    async with async_session() as session:
        try:
            await session.execute(text("PRAGMA foreign_keys = ON"))
            query = text("""
                CREATE TABLE IF NOT EXISTS user_achievements (
                    user_id         INTEGER,
                    achievement_id  INTEGER,
                    received_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    PRIMARY KEY (user_id, achievement_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE
                )
            """)
            await session.execute(query)
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при создании таблицы user_achievements: {e}")
            return False

async def create_user_achievement_progress_table() -> bool:
    async with async_session() as session:
        try:
            await session.execute(text("PRAGMA foreign_keys = ON"))
            query = text("""
                CREATE TABLE IF NOT EXISTS user_achievement_progress (
                    user_id         INTEGER,
                    achievement_id  INTEGER,
                    progress_value  INTEGER DEFAULT 0,
                    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    PRIMARY KEY (user_id, achievement_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE
                )
            """)
            await session.execute(query)
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при создании таблицы user_achievement_progress: {e}")
            return False

async def insert_achievements() -> bool:
    async with async_session() as session:
        try:
            for ach in ACHIEVEMENTS:
                await session.execute(
                    text("""
                        INSERT OR IGNORE INTO achievements (code, title, description, reward, target, event)
                        VALUES (:code, :title, :description, :reward, :target, :event)
                    """),
                    {
                        "code": ach["code"],
                        "title": ach["title"],
                        "description": ach["description"],
                        "reward": ach["reward"],
                        "target": ach["target"],
                        "event": ach["event"]
                    }
                )
            await session.commit()
            print("Достижения успешно добавлены.")
            return True
        except Exception as e:
            print(f"Ошибка при вставке достижений: {e}")
            return False

async def get_achievement_by_code(code: str):
    async with async_session() as session:
        result = await session.execute(
            text("SELECT * FROM achievements WHERE code = :code"),
            {"code": code}
        )
        row = result.mappings().first()  # Используем mappings() для доступа по имени
        return row


async def has_user_achievement(user_id: int, code: str):
    async with async_session() as session:
        result = await session.execute(
            text("""
                SELECT 1 FROM user_achievements
                WHERE user_id = :uid AND achievement_id = (
                    SELECT id FROM achievements WHERE code = :code
                )
            """),
            {"uid": user_id, "code": code}
        )
        return result.fetchone() is not None


async def get_user_achievement_progress(user_id: int, code: str):
    async with async_session() as session:
        result = await session.execute(
            text("""
                SELECT progress_value FROM user_achievement_progress
                WHERE user_id = :uid AND achievement_id = (
                    SELECT id FROM achievements WHERE code = :code
                )
            """),
            {"uid": user_id, "code": code}
        )
        row = result.fetchone()
        return row[0] if row else 0


async def set_user_achievement_progress(user_id: int, code: str, value: int):
    async with async_session() as session:
        await session.execute(
            text("""
                INSERT INTO user_achievement_progress (user_id, achievement_id, progress_value)
                VALUES (:uid, (SELECT id FROM achievements WHERE code = :code), :val)
                ON CONFLICT(user_id, achievement_id)
                DO UPDATE SET progress_value = :val, updated_at = CURRENT_TIMESTAMP
            """),
            {"uid": user_id, "code": code, "val": value}
        )
        await session.commit()


async def grant_user_achievement(user_id: int, code: str, reward: int):
    async with async_session() as session:
        await session.execute(
            text("""
                INSERT INTO user_achievements (user_id, achievement_id)
                VALUES (:uid, (SELECT id FROM achievements WHERE code = :code))
            """),
            {"uid": user_id, "code": code}
        )
        await session.execute(
            text("""
                UPDATE users SET dewin_coins = dewin_coins + :reward
                WHERE user_id = :uid
            """),
            {"reward": reward, "uid": user_id}
        )
        await session.commit()

async def get_full_achievement_status(user_id: int) -> list[dict]:
    async with async_session() as session:
        result = await session.execute(
            text("""
                SELECT 
                    a.code,
                    a.title,
                    a.description,
                    a.reward,
                    a.target,
                    COALESCE(uap.progress_value, CASE WHEN ua.received_at IS NOT NULL THEN a.target ELSE 0 END) as progress,
                    ua.received_at IS NOT NULL AS completed
                FROM achievements a
                LEFT JOIN user_achievements ua 
                    ON ua.achievement_id = a.id AND ua.user_id = :uid
                LEFT JOIN user_achievement_progress uap 
                    ON uap.achievement_id = a.id AND uap.user_id = :uid
                ORDER BY a.id
            """).columns(
                code=String,
                title=String,
                description=String,
                reward=Integer,
                target=Integer,
                progress=Integer,
                completed=Boolean
            ),
            {"uid": user_id}
        )

        rows = result.mappings().all()

        return [
            {
                "code": row["code"],
                "title": row["title"],
                "description": row["description"],
                "reward": row["reward"],
                "target": row["target"],
                "progress": row["progress"],
                "completed": bool(row["completed"]),
                "icon": f"/img/achivments/{get_icon_for_code(row['code'])}"
            }
            for row in rows
        ]

async def add_group_record(group_id: int, title: str, avatar_url: str = None) -> bool:
    """
    Добавляет новую группу в таблицу groups, если она ещё не существует.
    Принимает путь/URL до аватара группы.

    Args:
        group_id: Telegram group ID
        title: название группы
        avatar_url: путь/URL к аватарке (может быть None)

    Returns:
        bool: True — добавлено, False — уже есть
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("SELECT 1 FROM groups WHERE group_id = :group_id"),
                {"group_id": group_id}
            )
            if result.scalar():
                return False

            await session.execute(
                text("""
                    INSERT INTO groups (group_id, title, avatar_url)
                    VALUES (:group_id, :title, :avatar_url)
                """),
                {"group_id": group_id, "title": title, "avatar_url": avatar_url}
            )
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при добавлении группы: {e}")
            return False


async def add_membership_record(
    group_id: int,
    user_id: int,
    admin_level: int = 0,
    sms: int = 0,
    exp: int = 0,
    reputation: int = 0,
    data_reg: str = None
) -> bool:
    """
    Добавляет запись в таблицу memberships (участие пользователя в группе).

    Args:
        group_id: ID группы
        user_id: ID пользователя
        admin_level: уровень администратора
        sms, exp, reputation: статистика
        data_reg: дата регистрации (если None — текущая)

    Returns:
        bool: True — добавлено, False — уже есть
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT 1 FROM memberships 
                    WHERE group_id = :group_id AND user_id = :user_id
                """),
                {"group_id": group_id, "user_id": user_id}
            )
            if result.scalar():
                return False

            data_reg = data_reg or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            await session.execute(
                text("""
                    INSERT INTO memberships (group_id, user_id, admin_level, data_reg, sms, exp, reputation)
                    VALUES (:group_id, :user_id, :admin_level, :data_reg, :sms, :exp, :reputation)
                """),
                {
                    "group_id": group_id,
                    "user_id": user_id,
                    "admin_level": admin_level,
                    "data_reg": data_reg,
                    "sms": sms,
                    "exp": exp,
                    "reputation": reputation
                }
            )
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при добавлении membership: {e}")
            return False


async def delete_muted_table() -> None:
    """
    Удаляет таблицу muted_users, если она существует.
    """
    async with async_session() as session:
        query = 'DROP TABLE IF EXISTS muted_users'
        await session.execute(text(query))
        await session.commit()


async def create_muted_table() -> None:
    async with async_session() as session:
        query = '''
        CREATE TABLE IF NOT EXISTS muted_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            group_id INTEGER,
            username TEXT,
            user_id INTEGER,
            until_date TEXT,
            comment TEXT,
            UNIQUE(group_id, user_id)  -- Уникальная пара
        )
        '''
        await session.execute(text(query))
        # Добавляем индексы для быстрого поиска
        await session.execute(text('CREATE INDEX IF NOT EXISTS idx_muted_users_group_user ON muted_users(group_id, user_id)'))
        await session.execute(text('CREATE INDEX IF NOT EXISTS idx_muted_users_until_date ON muted_users(until_date)'))
        await session.commit()

async def mute_user(group_name: str, group_id: int, user_id: int, username: str, until_date: str, comment: str) -> None:
    """
    Добавляет замученного пользователя в базу данных.

    Args:
        group_id: ID группы в Telegram.
        user_id: ID пользователя в Telegram.
        username: Username пользователя.
        until_date: Дата, до которой пользователь замучен.
        comment: Причина мута.
    """
    
    if username is None:
        username = str(user_id)  # Используем user_id, если username отсутствует
    async with async_session() as session:
        query = '''
        INSERT INTO muted_users (group_name, group_id, username, user_id, until_date, comment)
        VALUES (:group_name, :group_id, :username, :user_id, :until_date, :comment)
        '''
        await session.execute(text(query), {
            "group_name": group_name,
            "group_id": group_id,
            "username": username,
            "user_id": user_id,
            "until_date": until_date,
            "comment": comment
        })
        await session.commit()

async def is_user_muted(group_id: int, user_id: int) -> bool:
    """
    Проверяет, замучен ли пользователь в данной группе.
    """
    async with async_session() as session:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = '''
        SELECT * FROM muted_users 
        WHERE group_id = :group_id 
        AND user_id = :user_id 
        AND until_date > :now
        '''
        result = await session.execute(text(query), {
            "group_id": group_id, 
            "user_id": user_id,
            "now": now
        })
        return result.first() is not None
    
async def ensure_muted_table_exists():
    async with async_session() as session:
        await session.execute(text('''
        CREATE TABLE IF NOT EXISTS muted_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            group_id INTEGER,
            username TEXT,
            user_id INTEGER,
            until_date TEXT,
            comment TEXT
        )
        '''))
        await session.commit()
    
async def unmute_user(group_id: int, user_id: int) -> None:
    """
    Удаляет пользователя из списка замученных.

    Args:
        group_id: ID группы в Telegram.
        user_id: ID пользователя в Telegram.
    """
    async with async_session() as session:
        query = '''
        DELETE FROM muted_users WHERE group_id = :group_id AND user_id = :user_id
        '''
        result = await session.execute(text(query), {"group_id": group_id, "user_id": user_id})
        await session.commit()
        return result.rowcount > 0  # Возвращает True, если была удалена хотя бы одна запись

async def delete_banned_table() -> None:
    """
    Удаляет таблицу ban_users, если она существует.
    """
    async with async_session() as session:
        query = 'DROP TABLE IF EXISTS ban_users'
        await session.execute(text(query))
        await session.commit()

async def create_banned_table() -> None:
    """
    Создает таблицу для забаненных пользователей, если она еще не существует.
    """
    # await delete_banned_table()
    async with async_session() as session:
        query = '''
        CREATE TABLE IF NOT EXISTS ban_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            group_id INTEGER,
            user_id INTEGER,
            username TEXT,
            until_date TEXT,
            reason TEXT
        )
        '''
        await session.execute(text(query))
        await session.commit()

async def ban_user(group_name: str, group_id: int, username: str, user_id: int, until_date: str, reason: str) -> None:
    """
    Добавляет забаненного пользователя в базу данных.
    """
    async with async_session() as session:
        # Удаляем предыдущие записи бана для этого пользователя
        delete_query = '''
        DELETE FROM ban_users WHERE group_id = :group_id AND user_id = :user_id
        '''
        await session.execute(text(delete_query), {"group_id": group_id, "user_id": user_id})
        # Добавляем новую запись
        query = '''
        INSERT INTO ban_users (group_name, group_id, username, user_id, until_date, reason)
        VALUES (:group_name, :group_id, :username, :user_id, :until_date, :reason)
        '''
        await session.execute(text(query), {
            "group_name": group_name,
            "group_id": group_id,
            "username": username,
            "user_id": user_id,
            "until_date": until_date,
            "reason": reason
        })
        await session.commit()

async def is_user_banned(group_id: int, user_id: int) -> bool:
    """
    Проверяет, забанен ли пользователь в данной группе.
    """
    async with async_session() as session:
        current_time = datetime.now()  # Получаем текущую дату как объект datetime
        
        logging.info(f"Проверка бана для user_id: {user_id}, group_id: {group_id}, current_time: {current_time}")
        
        query = '''
        SELECT * FROM ban_users 
        WHERE group_id = :group_id AND user_id = :user_id AND until_date > :current_time
        '''
        result = await session.execute(text(query), {"group_id": group_id, "user_id": user_id, "current_time": current_time})
        
        if result.first() is not None:
            logging.info("Пользователь забанен.")
            return True
        else:
            logging.info("Пользователь не в бане.")
            return False

async def get_ban_info(group_id: int, user_id: int) -> tuple:
    """
    Возвращает информацию о бане пользователя (дата разбана и причина).
    """
    async with async_session() as session:
        query = '''
        SELECT until_date, reason FROM ban_users 
        WHERE group_id = :group_id AND user_id = :user_id 
        ORDER BY until_date DESC 
        LIMIT 1
        '''
        result = await session.execute(text(query), {"group_id": group_id, "user_id": user_id})
        ban_info = result.first()
        return ban_info if ban_info else (None, None)

async def unban_user(group_id: int, user_id: int) -> None:
    """
    Удаляет пользователя из списка забаненных.

    Args:
        group_id: ID группы в Telegram.
        user_id: ID пользователя в Telegram.
    """
    async with async_session() as session:
        query = '''
        DELETE FROM ban_users WHERE group_id = :group_id AND user_id = :user_id
        '''
        await session.execute(text(query), {"group_id": group_id, "user_id": user_id})
        await session.commit()

async def delete_table_by_name(table_name: str) -> bool:
    async with async_session() as session:
        try:
            check_query = f'SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}";'
            result = await session.execute(text(check_query))
            if not result.first():
                print(f"Таблица {table_name} не найдена.")
                return False
            
            query = f'DROP TABLE IF EXISTS "{table_name}"'
            await session.execute(text(query))
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении таблицы {table_name}: {e}")
            return False

# async def add_user(group_id: int, user_id: int, username: str, admin_level: int, data_reg: str, exp: int, reputation: int) -> None:
#     """
#     Функция для добавления в таблицу группы юзера. Для успешного созадния необходимо передать все данные
#     в соотвествии с ожидаемым типом данных

#     Args:
#         group_id: id группы в telegram 
#         user_id: id пользователя в telegram
#         username: юзернейм пользователя 
#         admin_level: уровень администратора
#         data_reg: дата регистрации пользователя в бд в конкретной таблице
#     Returns:
#         bool: True - если пользователя не было и была создана запись в бд, False - елси пользователь был в бд и запись не сделана
#     """
#     async with async_session() as session:
#         query = f'SELECT * FROM "tgr_{group_id}" WHERE user_id = {user_id}'
#         user = await session.execute(text(query))
#         user = user.mappings().all()
#         if user == []:
#             query = f'INSERT INTO "tgr_{group_id}" VALUES ({user_id}, "{username}", {admin_level}, "{data_reg}", 0, {exp}, {reputation})'
#             await session.execute(text(query))
#             await session.commit()
#             return True
#         elif user != []:
#             return False

async def add_user_record(user_id: int, username: str, avatar_url: str = None) -> bool:
    """
    Добавляет нового пользователя в таблицу users, если он ещё не существует.

    Args:
        user_id: Telegram user ID
        username: username пользователя
        avatar_url: путь или URL к аватарке (опционально)

    Returns:
        bool: True — если пользователь был добавлен, False — если уже существует
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("SELECT 1 FROM users WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            if result.scalar():
                return False

            await session.execute(
                text("""
                    INSERT INTO users (user_id, username, avatar_url)
                    VALUES (:user_id, :username, :avatar_url)
                """),
                {"user_id": user_id, "username": username, "avatar_url": avatar_url}
            )
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при добавлении пользователя: {e}")
            return False

async def add_message(
    group_id: int,
    user_id: int,
    username: str = None,
    avatar_url: str = None
) -> None:
    """
    В ходе поступающего сообщения:
    - Если пользователя ещё нет в базе пользователей — добавляем
    - Если пользователя ещё нет в группе — добавляем с нулевой статистикой
    - В противном случае увеличиваем количество сообщений и опыта.
    """
    async with async_session() as session:
        try:
            async with session.begin():
                # В базе пользователей?
                result = await session.execute(
                    text("SELECT 1 FROM users WHERE user_id = :user_id"),
                    {"user_id": user_id}
                )
                if not result.scalar():
                    # Вставляем пользователя
                    await add_user_record(user_id, username or f"user{user_id}", avatar_url)

                # В группе?
                result = await session.execute(
                    text("SELECT 1 FROM memberships WHERE group_id = :group_id AND user_id = :user_id"),
                    {"group_id": group_id, "user_id": user_id}
                )
                if not result.scalar():
                    # Вставляем с нулевой статистикой
                    await add_membership_record(
                        group_id=group_id,
                        user_id=user_id,
                        admin_level=0,
                        sms=0,
                        exp=0,
                        reputation=0,
                        data_reg=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )

                # Обновляем количество сообщений и опыта
                await session.execute(
                    text("""
                        UPDATE memberships
                        SET sms = sms + 1,
                            exp = exp + 2
                        WHERE group_id = :group_id AND user_id = :user_id
                    """),
                    {"group_id": group_id, "user_id": user_id}
                )

                # В крайнем случае можем также проапдейтить имя пользователя
                if username:
                    await session.execute(
                        text("""
                            UPDATE users
                            SET username = :username
                            WHERE user_id = :user_id
                        """),
                        {"username": username, "user_id": user_id}
                    )

        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка в add_message: {e}")

            
async def get_stat() -> list:
    """
    Собирает статистику из новых таблиц:
    - Кол-во зарегистрированных групп
    - Кол-во уникальных пользователей
    - Общее количество сообщений по всем группам

    Returns:
        list: [кол-во групп, кол-во пользователей, общее кол-во сообщений]
    """
    async with async_session() as session:
        try:
            # 1. Кол-во групп
            result = await session.execute(text("SELECT COUNT(*) FROM groups"))
            group_count = result.scalar() or 0

            # 2. Кол-во уникальных пользователей
            result = await session.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar() or 0

            # 3. Общее количество сообщений
            result = await session.execute(text("SELECT SUM(sms) FROM memberships"))
            sms_count = result.scalar() or 0

            return [group_count, user_count, sms_count]
        except Exception as e:
            print(f"❌ Ошибка при получении статистики: {e}")
            return [0, 0, 0]

async def get_banned_users(group_id: int):
    async with async_session() as session:
        query = '''
        SELECT user_id, username, until_date, reason FROM ban_users 
        WHERE group_id = :group_id
        '''
        result = await session.execute(text(query), {"group_id": group_id})
        return result.fetchall()

async def update_group_settings(update: GroupUpdate) -> bool:
    """
    Обновляет указанные поля в таблице groups, используя объект GroupUpdate.

    Args:
        update (GroupUpdate): объект с полями, которые нужно обновить

    Returns:
        bool: True — если обновление прошло успешно, False — если не было данных для обновления
    """
    async with async_session() as session:
        try:
            fields_to_update = []
            params = {"group_id": update.group_id}

            for field_name, value in vars(update).items():
                if field_name == "group_id" or value is None:
                    continue
                fields_to_update.append(f"{field_name} = :{field_name}")
                params[field_name] = value

            if not fields_to_update:
                return False

            query = f'''
                UPDATE groups
                SET {", ".join(fields_to_update)}
                WHERE group_id = :group_id
            '''
            await session.execute(text(query), params)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при обновлении настроек группы: {e}")
            return False

async def check_and_update_group_title(group_id: int, current_title: str) -> None:
    """
    Проверяет, изменилось ли название группы. Если изменилось — обновляет в таблице groups.

    Args:
        group_id (int): ID группы
        current_title (str): Текущее название, полученное из Telegram
    """
    async with async_session() as session:
        try:
            # Получить сохранённое название из БД
            result = await session.execute(
                text("SELECT title FROM groups WHERE group_id = :group_id"),
                {"group_id": group_id}
            )
            db_record = result.mappings().first()

            if not db_record:
                print(f"Ошибка при обновлении имени группы.Группы {group_id} не существует: {e}")
                return

            saved_title = db_record['title']
            if saved_title != current_title:
                await session.execute(
                    text("UPDATE groups SET title = :title WHERE group_id = :group_id"),
                    {"title": current_title, "group_id": group_id}
                )
                await session.commit()
                print(f"🔄 Название группы обновлено: '{saved_title}' → '{current_title}'")
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при проверке названия группы: {e}")

async def get_muted_users(group_id: int):
    async with async_session() as session:
        query = '''
        SELECT user_id, username, until_date, comment 
        FROM muted_users 
        WHERE group_id = :group_id
        ORDER BY until_date
        '''
        result = await session.execute(text(query), {"group_id": group_id})
        return result.fetchall()

async def get_admin_level(user_id: int, group_id: int) -> int:
    """
    Получает уровень администратора пользователя в заданной группе из таблицы memberships.

    Args:
        user_id (int): Telegram ID пользователя.
        group_id (int): Telegram ID группы.

    Returns:
        int: Уровень администратора (0, если пользователь не найден).
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT admin_level
                    FROM memberships
                    WHERE group_id = :group_id AND user_id = :user_id
                """),
                {"group_id": group_id, "user_id": user_id}
            )
            admin_level = result.scalar()
            return admin_level if admin_level is not None else 0
        except Exception as e:
            print(f"❌ Ошибка при получении admin_level: {e}")
            return 0

async def get_user_level(exp: int) -> str:
    levels = [
        (50, "Новичок"), (150, "Ученик"), (300, "Знаток"),
        (500, "Профи"), (700, "Мастер"), (1000, "Мыслитель"),
        (1300, "Мудрец"), (2000, "Просветленный"), (float('inf'), "Высший разум")
    ]
    for threshold, level in levels:
        if exp < threshold:
            return level
    return "Высший разум"

async def update_reputation(group_id: int, user_id: int, change: int) -> bool:
    """
    Обновляет репутацию пользователя в заданной группе.

    Args:
        group_id (int): ID группы
        user_id (int): ID пользователя
        change (int): Сколько прибавить или убавить к текущей репутации

    Returns:
        bool: True — если обновлено, False — если пользователь не найден
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT reputation
                    FROM memberships
                    WHERE group_id = :group_id AND user_id = :user_id
                """),
                {"group_id": group_id, "user_id": user_id}
            )
            current_reputation = result.scalar()

            if current_reputation is None:
                print(f"⚠️ Пользователь {user_id} не найден в группе {group_id}")
                return False

            new_reputation = current_reputation + change
            print(f"📝 Обновляю репутацию: {user_id} → {current_reputation} ➜ {new_reputation}")

            await session.execute(
                text("""
                    UPDATE memberships
                    SET reputation = :new_reputation
                    WHERE group_id = :group_id AND user_id = :user_id
                """),
                {
                    "new_reputation": new_reputation,
                    "group_id": group_id,
                    "user_id": user_id
                }
            )
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при обновлении репутации: {e}")
            return False

    
async def get_user_info(group_id: int, user_id: int):
    """
    Возвращает информацию о пользователе в контексте конкретной группы, включая username, статистику и роль.

    Args:
        group_id (int): Telegram ID группы
        user_id (int): Telegram ID пользователя

    Returns:
        dict | None: Словарь с данными пользователя, либо None, если пользователь не найден в группе
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT 
                        u.user_id,
                        u.username,
                        u.avatar_url,
                        u.dewin_coins,
                        u.subscription_till,
                        u.registered,
                        m.admin_level,
                        m.data_reg,
                        m.sms,
                        m.exp,
                        m.reputation
                    FROM memberships m
                    JOIN users u ON u.user_id = m.user_id
                    WHERE m.group_id = :group_id AND m.user_id = :user_id
                """),
                {"group_id": group_id, "user_id": user_id}
            )
            return result.mappings().first()
        except Exception as e:
            print(f"❌ Ошибка при получении информации о пользователе: {e}")
            return None


async def get_reputation(group_id: int, user_id: int) -> int:
    """
    Получает репутацию пользователя в заданной группе из таблицы memberships.

    Args:
        group_id (int): ID группы в Telegram.
        user_id (int): ID пользователя в Telegram.

    Returns:
        int: Репутация пользователя. Если пользователь не найден, возвращается 0.
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT reputation
                    FROM memberships
                    WHERE group_id = :group_id AND user_id = :user_id
                """),
                {"group_id": group_id, "user_id": user_id}
            )
            reputation = result.scalar()
            return reputation if reputation is not None else 0
        except Exception as e:
            print(f"❌ Ошибка при получении репутации: {e}")
            return 0


async def create_marriages_table() -> None:
    async with async_session() as session:
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS "marriages" (
                marriage_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER,
                user2_id INTEGER,
                group_id INTEGER,
                date_of_marriage TEXT
            )
            '''
            await session.execute(text(query))
            await session.commit()
            print('Таблица создана!')
        except Exception as e:
            print(f"Ошибка при создании таблицы браков: {e}")


async def create_marriage(user1_id: int, user2_id: int, group_id: int) -> bool:
    """Создание нового брака"""
    # Создаем таблицу браков, если она еще не существует
    await create_marriages_table()

    async with async_session() as session:
        try:
            # Проверка, не состоят ли уже пользователи в браке в этой группе
            query = f'''
            SELECT * FROM marriages 
            WHERE (user1_id = {user1_id} AND user2_id = {user2_id} AND group_id = {group_id}) 
               OR (user1_id = {user2_id} AND user2_id = {user1_id} AND group_id = {group_id})
            '''
            result = await session.execute(text(query))
            existing_marriage = result.mappings().all()

            if existing_marriage:
                print(f"Пользователи {user1_id} и {user2_id} уже состоят в браке в группе {group_id}.")
                return False

            # Если брака нет, создаем новый
            date_of_marriage = datetime.now().strftime('%H:%M %d.%m.%y')
            insert_query = f'''
            INSERT INTO marriages (user1_id, user2_id, group_id, date_of_marriage)
            VALUES ({user1_id}, {user2_id}, {group_id}, "{date_of_marriage}")
            '''
            await session.execute(text(insert_query))
            await session.commit()
            print(f"Брак между {user1_id} и {user2_id} успешно заключен в группе {group_id}.")
            return True
        except Exception as e:
            print(f"Ошибка при заключении брака: {e}")
            return False


async def check_marriage(user_id: int, group_id: int) -> int:
    async with async_session() as session:
        query = f'''
        SELECT marriage_id FROM marriages 
        WHERE (user1_id = {user_id} OR user2_id = {user_id}) 
        AND group_id = {group_id}
        '''
        result = await session.execute(text(query))
        marriage = result.mappings().all()
        if marriage:
            return marriage[0]['marriage_id']  # Возвращаем ID брака, если найден
        return None  # Если брака нет, возвращаем None

async def get_marriage(group_id: int, user_id: int):
    """
    Получает информацию о браке пользователя в конкретной группе.

    Args:
        group_id (int): Telegram ID группы.
        user_id (int): Telegram ID пользователя.

    Returns:
        dict | None: Информация о браке (marriage_id, user1_id, user2_id), либо None, если не найден.
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT marriage_id, user1_id, user2_id 
                    FROM marriages 
                    WHERE (user1_id = :user_id OR user2_id = :user_id)
                    AND group_id = :group_id
                """),
                {"user_id": user_id, "group_id": group_id}
            )
            return result.mappings().first()
        except Exception as e:
            print(f"❌ Ошибка при получении брака: {e}")
            return None

async def kick_user(bot: Bot, chat_id: int, user_id: int):
    try:
        await bot.kick_chat_member(chat_id, user_id)
        print(f"Пользователь {user_id} был исключен из группы {chat_id}.")
    except Exception as e:
        print(f"Ошибка при исключении пользователя {user_id}: {e}")
        
async def get_admin_groups(user_id: int) -> list:
    """
    Возвращает список group_id, где пользователь является администратором 4 уровня.

    Args:
        user_id (int): Telegram ID пользователя.

    Returns:
        list: Список group_id, где пользователь является администратором 4 уровня.
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT group_id
                    FROM memberships
                    WHERE user_id = :user_id AND admin_level = 4
                """),
                {"user_id": user_id}
            )
            return result.scalars().all()
        except Exception as e:
            print(f"❌ Ошибка при получении админ-групп: {e}")
            return []

async def migrate_old_tables_to_new_format():
    async with async_session() as session:
        try:
            # Включаем поддержку внешних ключей в SQLite
            await session.execute(text("PRAGMA foreign_keys = ON"))

            # Получаем все таблицы вида tgr_*
            result = await session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'tgr_%';")
            )
            tables = result.scalars().all()
            print(tables)

            for table in tables:
                # Извлекаем group_id из названия таблицы
                match = re.match(r'tgr_-(\d+)', table)
                if not match:
                    continue
                group_id = int(match.group(1))

                # Добавляем группу
                await add_group_record(group_id, title=f"Group {group_id}")

                # Получаем пользователей
                result = await session.execute(text(f'SELECT * FROM "{table}"'))
                rows = result.mappings().all()

                for row in rows:
                    user_id = row.get("user_id")
                    username = row.get("username") or "no_username"
                    admin_level = row.get("admin_level", 0)
                    data_reg = row.get("data_reg")
                    sms = row.get("sms", 0)
                    exp = row.get("exp", 0)
                    reputation = row.get("reputation", 0)

                    # Добавляем пользователя
                    await add_user_record(user_id, username)

                    # Добавляем membership
                    await add_membership_record(
                        group_id=group_id,
                        user_id=user_id,
                        admin_level=admin_level,
                        data_reg=data_reg,
                        sms=sms,
                        exp=exp,
                        reputation=reputation
                    )

            await session.commit()
            print("✅ Миграция завершена")

        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при миграции: {e}")

async def remove_membership_record(group_id: int, user_id: int) -> bool:
    """
    Удаляет пользователя из группы (таблица memberships).

    Args:
        group_id: ID группы
        user_id: ID пользователя

    Returns:
        bool: True — если удалено, False — если записи не было
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    DELETE FROM memberships 
                    WHERE group_id = :group_id AND user_id = :user_id
                """),
                {"group_id": group_id, "user_id": user_id}
            )
            await session.commit()
            return result.rowcount > 0
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при удалении membership: {e}")
            return False

async def remove_user_record(user_id: int) -> bool:
    """
    Удаляет пользователя из таблицы users (и все его связи, если включён ON DELETE CASCADE).

    Args:
        user_id: Telegram user ID

    Returns:
        bool: True — если удалён, False — если не найден
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("DELETE FROM users WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            await session.commit()
            return result.rowcount > 0
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при удалении пользователя: {e}")
            return False

async def get_admins(group_id: int, level: int):
    """
    Возвращает список администраторов заданного уровня в конкретной группе.

    Args:
        group_id (int): ID группы в Telegram.
        level (int): Уровень администратора.

    Returns:
        list: Список словарей с user_id и username.
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT u.user_id, u.username
                    FROM memberships m
                    JOIN users u ON u.user_id = m.user_id
                    WHERE m.group_id = :group_id AND m.admin_level = :level
                """),
                {"group_id": group_id, "level": level}
            )
            return result.mappings().all()
        except Exception as e:
            print(f"❌ Ошибка при получении администраторов уровня {level}: {e}")
            return []

async def get_top_users(group_id: int) -> list:
    """
    Возвращает топ-10 пользователей по количеству сообщений в заданной группе.

    Args:
        group_id (int): Telegram ID группы.

    Returns:
        list: Список словарей с user_id, username и sms.
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT 
                        u.user_id,
                        u.username,
                        m.sms
                    FROM memberships m
                    JOIN users u ON u.user_id = m.user_id
                    WHERE m.group_id = :group_id
                    ORDER BY m.sms DESC
                    LIMIT 10
                """),
                {"group_id": group_id}
            )
            return result.mappings().all()
        except Exception as e:
            print(f"❌ Ошибка при получении топа пользователей: {e}")
            return []

async def get_username_by_id(user_id: int, group_id: int) -> str:
    """
    Возвращает username пользователя по его ID в конкретной группе.

    Args:
        user_id (int): Telegram ID пользователя.
        group_id (int): Telegram ID группы.

    Returns:
        str: Username, если найден. Иначе — "Неизвестный".
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT u.username
                    FROM memberships m
                    JOIN users u ON u.user_id = m.user_id
                    WHERE m.user_id = :user_id AND m.group_id = :group_id
                """),
                {"user_id": user_id, "group_id": group_id}
            )
            username = result.scalar()
            return username or "Неизвестный"
        except Exception as e:
            print(f"❌ Ошибка при получении username: {e}")
            return "Неизвестный"

async def get_all_users_in_group(group_id: int) -> list:
    """
    Получает список всех пользователей в указанной группе.

    Args:
        group_id (int): Telegram ID группы.

    Returns:
        list: Список словарей с user_id и username.
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("""
                    SELECT u.user_id, u.username
                    FROM memberships m
                    JOIN users u ON u.user_id = m.user_id
                    WHERE m.group_id = :group_id
                """),
                {"group_id": group_id}
            )
            return result.mappings().all()
        except Exception as e:
            print(f"❌ Ошибка при получении пользователей группы {group_id}: {e}")
            return []

async def upsert_user(user_id: int, username: str, avatar_url: str = None) -> bool:
    """
    Добавляет нового пользователя или обновляет поле `registered`, если оно отсутствует.

    Args:
        user_id: Telegram user ID
        username: Telegram username
        avatar_url: URL или путь к аватарке

    Returns:
        bool: True, если пользователь был добавлен или обновлён, False — если произошла ошибка
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                text("SELECT registered FROM users WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            row = result.fetchone()

            if row is None:
                # Пользователя нет — добавляем
                await session.execute(
                    text("""
                        INSERT INTO users (user_id, username, avatar_url, registered)
                        VALUES (:user_id, :username, :avatar_url, :registered)
                    """),
                    {
                        "user_id": user_id,
                        "username": username,
                        "avatar_url": avatar_url,
                        "registered": datetime.utcnow()
                    }
                )
            else:
                # Пользователь есть, проверим registered
                if row["registered"] is None:
                    await session.execute(
                        text("""
                            UPDATE users
                            SET registered = :registered
                            WHERE user_id = :user_id
                        """),
                        {
                            "registered": datetime.utcnow(),
                            "user_id": user_id
                        }
                    )

            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            print(f"Ошибка в upsert_user: {e}")
            return False

async def get_platform_statistics():
    async with async_session() as session:
        result = await session.execute(
            text("""
                SELECT
                    (SELECT COUNT(DISTINCT user_id) FROM memberships) AS user_count,
                    (SELECT COUNT(*) FROM groups) AS group_count
            """)
        )
        row = result.fetchone()
        return {
            "users": row.user_count,
            "groups": row.group_count
        }

async def get_user_profile(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            text("""
                SELECT user_id, username, avatar_url, dewin_coins, subscription_till
                FROM users
                WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        )
        row = result.fetchone()
        if row is None:
            return None
        return {
            "user_id": row.user_id,
            "username": row.username,
            "avatar_url": row.avatar_url,
            "coins": row.dewin_coins,
            "subscription_till": row.subscription_till
        }

async def get_user_groups(user_id: int):
    async with async_session() as session:
        result = await session.execute(text("""
            SELECT 
                g.group_id,
                g.title,
                g.avatar_url,
                m.admin_level,
                m.reputation,
                m.sms AS messages
            FROM memberships m
            JOIN groups g ON m.group_id = g.group_id
            WHERE m.user_id = :uid
        """), {"uid": user_id})
        return result.mappings().all()

async def get_owned_groups(user_id: int):
    async with async_session() as session:
        result = await session.execute(text("""
            SELECT 
                g.group_id,
                g.title,
                g.avatar_url,
                m.reputation,
                m.sms AS messages
            FROM memberships m
            JOIN groups g ON m.group_id = g.group_id
            WHERE m.user_id = :uid AND m.admin_level = 4
        """), {"uid": user_id})
        return result.mappings().all()

async def get_total_messages(user_id: int):
    async with async_session() as session:
        result = await session.execute(text("""
            SELECT SUM(sms) FROM memberships WHERE user_id = :uid
        """), {"uid": user_id})
        return result.scalar() or 0

async def get_user_group_settings(user_id: int) -> GroupSettingsResponse:
    async with async_session() as session:
        # Получение групп
        result = await session.execute(text("""
            SELECT
                g.group_id,
                g.title,
                g.avatar_url,
                g.night_mode_enabled,
                g.antispam_enabled,
                g.language
            FROM groups g
            JOIN memberships m ON g.group_id = m.group_id
            WHERE m.user_id = :uid AND m.admin_level = 4
        """), {"uid": user_id})

        rows = result.fetchall()

        # Получение премиума
        premium_result = await session.execute(text("""
            SELECT subscription_till FROM users WHERE user_id = :uid
        """), {"uid": user_id})
        till = premium_result.scalar()
        if till is not None:
            try:
                till_dt = datetime.fromisoformat(till)
            except ValueError:
                till_dt = datetime.strptime(till, "%Y-%m-%d %H:%M:%S")
        else:
            till_dt = None

        is_premium = till_dt is not None and till_dt > datetime.utcnow()
        is_premium = True
        return GroupSettingsResponse(
            is_premium=is_premium,
            groups=[
                GroupSettingsOut(
                    group_id=row.group_id,
                    title=row.title,
                    avatar_url=row.avatar_url or "",
                    night_mode=bool(row.night_mode_enabled),
                    anti_spam=bool(row.antispam_enabled),
                    language=row.language,
                )
                for row in rows
            ]
        )

async def apply_group_settings_update(user_id: int, data: GroupSettingsUpdate) -> bool:
    async with async_session() as session:
        # Проверка прав
        check = await session.execute(text("""
            SELECT 1 FROM memberships
            WHERE user_id = :uid AND group_id = :gid AND admin_level = 4
        """), {"uid": user_id, "gid": data.group_id})

        if not check.scalar():
            return False  # Нет доступа

        fields = []
        params = {"gid": data.group_id}

        if data.night_mode is not None:
            fields.append("night_mode_enabled = :night_mode_enabled")
            params["night_mode_enabled"] = int(data.night_mode)
        if data.anti_spam is not None:
            fields.append("antispam_enabled = :antispam_enabled")
            params["antispam_enabled"] = int(data.anti_spam)
        if data.language is not None:
            fields.append("language = :language")
            params["language"] = data.language

        if not fields:
            return True  # Нечего обновлять

        query = f"""
            UPDATE groups SET {', '.join(fields)}
            WHERE group_id = :gid
        """
        await session.execute(text(query), params)
        await session.commit()
        return True

async def get_group_info_from_db(group_id: int) -> dict | None:
    """
    Возвращает все настройки группы по group_id.
    """
    async with async_session() as session:
        try:
            query = text("SELECT * FROM groups WHERE group_id = :group_id")
            result = await session.execute(query, {"group_id": group_id})
            row = result.fetchone()
            if not row:
                return None
            return dict(row._mapping)
        except Exception as e:
            print(f"Ошибка при получении информации о группе: {e}")
            return None
async def update_welcome_message_in_db(group_id: int, message: str) -> bool:
    """
    Обновляет приветственное сообщение для заданной группы.
    """
    async with async_session() as session:
        try:
            query = text("""
                UPDATE groups
                SET welcome_message = :message
                WHERE group_id = :group_id
            """)
            await session.execute(query, {"group_id": group_id, "message": message})
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении welcome_message: {e}")
            return False

async def update_farewell_message_in_db(group_id: int, message: str) -> bool:
    async with async_session() as session:
        try:
            query = text("""
                UPDATE groups
                SET farewell_message = :message
                WHERE group_id = :group_id
            """)
            await session.execute(query, {"group_id": group_id, "message": message})
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении farewell_message: {e}")
            return False

async def update_banned_words_in_db(group_id: int, words: list[str], action: str) -> bool:
    async with async_session() as session:
        try:
            query = text("""
                UPDATE groups
                SET banned_words = :words, banned_words_action = :action
                WHERE group_id = :group_id
            """)
            await session.execute(query, {
                "group_id": group_id,
                "words": json.dumps(words),
                "action": action
            })
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении banned_words: {e}")
            return False

async def update_link_whitelist_in_db(group_id: int, links: list[str], action: str) -> bool:
    async with async_session() as session:
        try:
            query = text("""
                UPDATE groups
                SET link_whitelist = :links, linked_whitelist_action = :action
                WHERE group_id = :group_id
            """)
            await session.execute(query, {
                "group_id": group_id,
                "links": json.dumps(links),
                "action": action
            })
            await session.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении link_whitelist: {e}")
            return False