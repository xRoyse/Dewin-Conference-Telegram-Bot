import asyncio
import aiogram
from aiogram import types
from datetime import datetime, timedelta

from sqlalchemy import text
from database.database import async_session, ensure_muted_table_exists, get_admin_level, get_muted_users, kick_user, mute_user, is_user_muted, unmute_user, remove_membership_record

from utils.loader import dew_channel, log_message_thread_id


data = datetime.now()

async def mute_handlers(bot, message: types.Message):
    await ensure_muted_table_exists()  
    admin_level = await get_admin_level(message.from_user.id, message.chat.id)
    
    if admin_level < 2:  
        await message.reply("<b>⛔ У вас недостаточно прав для использования этой команды.</b>", parse_mode="HTML")
        return
    
    if not message.reply_to_message:
        await message.reply("<b>⛔ Эта команда должна быть ответом на сообщение!</b>", parse_mode='html')
        return

    try:
        muteint = int(message.text.split()[1])
        mutetype = message.text.split()[2]
        comment = " ".join(message.text.split()[3:])
    except (IndexError, ValueError):
        await message.reply('<b>Не хватает аргументов или неверный формат!\n\nПример:</b>\n<blockquote>/мут 1 ч причина</blockquote>', parse_mode='html')
        return

    # Устанавливаем время мута
    if mutetype in ["ч", "час", "часов"]:
        until_date = datetime.now() + timedelta(hours=muteint)
    elif mutetype in ["м", "мин", "минут", "минуты"]:
        until_date = datetime.now() + timedelta(minutes=muteint)
    elif mutetype in ["д", "день", "дней"]:
        until_date = datetime.now() + timedelta(days=muteint)
    else:
        await message.reply("<b>Неверный тип времени. Используйте 'ч', 'м' или 'д'</b>", parse_mode='html')
        return

    # Проверяем, замучен ли пользователь
    group_name = message.chat.title
    user_id = message.reply_to_message.from_user.id
    user_admin_level = await get_admin_level(user_id, message.chat.id)
    username = message.reply_to_message.from_user.username or 'No username'  # Используем No username, если username отсутствует


    if await is_user_muted(message.chat.id, user_id):
        await message.reply("<b>🚫 Этот пользователь уже замучен.</b>", parse_mode='html')
        return

    if not comment:
        await message.reply("<b>❌ Причина мута не может быть пустой!</b>",parse_mode='html')
        return
    
    if user_id == message.from_user.id:
        await message.reply("<b>❌ Вы не можете замьютить самого себя!</b>", parse_mode='html')
        return

    if user_admin_level > admin_level:
        await message.reply("<b>❌ Вы не можете замьютить пользователя с более высоким уровнем админа!</b>", parse_mode='html')
        return

    # Мутим пользователя
    await mute_user(group_name, message.chat.id, user_id, username, until_date.strftime('%Y-%m-%d %H:%M:%S'), comment)
    await bot.send_message(
        dew_channel, 
        f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
        f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> заблокировал чат (замутил) пользователя <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a></b>"
        f"<blockquote><b>Дата разблокировки:</b> <code>{until_date.strftime('%Y-%m-%d %H:%M:%S')}</code>\n"
        f"<b>Причина:</b> <code>{comment}</code></blockquote>\n"
        f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n",
        parse_mode="HTML", message_thread_id=log_message_thread_id
    )

    # Отправляем личное сообщение пользователю
    try:
        print(f"Добавлен мут для {user_id} в группе {group_name}. Дата: {until_date}")
        await bot.send_photo(
            chat_id=user_id,
            photo=open('media/photos/Замьючен.png', 'rb'),
            caption=(
                    f"<b>Вам выдали блокировку чата в группе <code>{message.chat.title}</code></b>\n\n"
                    f"<b>Выдал:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n"
                    f"<b>Выдано до:</b> <code>{until_date.strftime('%Y-%m-%d %H:%M:%S')}</code>\n\n"
                    f"<b>Причина:</b> <code>{comment}</code>"
                ), parse_mode='html'
            )
    except Exception as e:
        # Логируем ошибку или просто пропускаем
        print(f"Не удалось отправить личное сообщение пользователю {user_id}: {e}")

    # Дополнительное сообщение для подтверждения
    with open('media/photos/Замьючен.png', 'rb') as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=(
                    f"<b>Пользователю <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> была выдана блокировка чата.</b>\n\n"
                    f"<b>Дата:</b> <code>{data.strftime('%H:%M %d-%m-%Y')}</code>\n"
                    f"<b>Выдал: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a></b>\n"
                    f"<b>Выдано до:</b> <code>{until_date.strftime('%Y-%m-%d %H:%M:%S')}</code>\n\n"
                    f"<b>Причина:</b> <code>{comment}</code>"
                ),
                parse_mode='HTML'
            )

async def check_muted_users(bot):
    while True:
        await asyncio.sleep(60)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        async with async_session() as session:
            query = '''
            SELECT * FROM muted_users WHERE until_date < :now
            '''
            result = await session.execute(text(query), {"now": now})
            muted_users = result.fetchall()

            for user in muted_users:
                group_id = user.group_id
                user_id = user.user_id
                username = user.username
                group_name = user.group_name

                await unmute_user(group_id, user_id)
                user_message_count.pop(user_id, None)
                await bot.send_message(
                    dew_channel,
                    f"<b>👥  Группа: <code>{group_name}</code></b>\n\n"
                    f"<b>👤 C пользователя <a href='tg://user?id={user_id}'>{username}</a> была снята блокировка чата (мут)</b>\n"
                    f"<b>💠 id пользователя: <code>{user_id}</code></b>\n\n",
                    parse_mode="HTML", message_thread_id=log_message_thread_id
                )


                # Отправляем сообщение пользователю
                try:
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=open('media/photos/Размьючен.png', 'rb'),
                        caption=(
                            f"<b>❗️ С вас была снята блокировка чата в группе</b> <code>{group_name}</code>\n\n"
                            f"<b>⚠️ Теперь вы вновь можете писать, больше не нарушайте!</b>"
                        ), parse_mode='html'
                    )
                except Exception as e:
                    print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


user_message_count = {}

async def message_handler(bot, message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Проверяем, является ли сообщение командой
    if message.text.startswith('/'):
        from utils.operators import handlers_commands
        await handlers_commands(bot, message)

    # Проверяем, замучен ли пользователь
    if await is_user_muted(chat_id, user_id):
        # Удаляем сообщение
        try:
            await message.delete()
        except aiogram.utils.exceptions.MessageCantBeDeleted:
            print("Не удалось удалить сообщение: сообщение не может быть удалено для всех.")
        except Exception as e:
            print(f"Произошла ошибка при удалении сообщения: {e}")


        # Увеличиваем счетчик сообщений
        if user_id not in user_message_count:
            user_message_count[user_id] = 0
        user_message_count[user_id] += 1


        # Отправляем предупреждение только при первом нарушении
        if user_message_count[user_id] == 1:
            await message.answer(
                f"<b>⚠️ <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>, вы находитесь в муте!\nНе пишите сообщения иначе будете исключены из группы!</b>",
                parse_mode='html'
            )
        # Если пользователь отправил 3 сообщения после предупреждения -> исключаем
        elif user_message_count[user_id] >= 3:
            await kick_user(bot, chat_id, user_id)
            await remove_membership_record(chat_id, user_id)
            try:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=open('media/photos/Кикнут.png', 'rb'),
                    caption=(
                            f"<b>Вы были исключены из группы <code>{message.chat.title}</code></b>\n\n"
                            f"<b>Причина:</b> <code>Нарушение правил группы</code>"
                        ), parse_mode='html'
                    )
            except Exception as e:
                # Логируем ошибку или просто пропускаем
                print(f"Не удалось отправить личное сообщение пользователю {user_id}: {e}")
                
            with open('media/photos/Кикнут.png', 'rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption=(
                        f"<b>Пользователь <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a> был исключен из группы за нарушение правил.\n\nНадеемся что больше никто не хочет нарушать правила, верно?</b>"
                    ),
                    parse_mode='HTML'
                )
                user_message_count.pop(user_id, None)  # Сбрасываем счетчик
