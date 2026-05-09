# handlers/commands.py

import logging
from aiogram import types, Dispatcher
from utils.shorten_api import get_shortened_link # Используем относительный импорт
from config import API_ENDPOINT # Импортируем для использования в сообщениях, если нужно
from utils.loader import dew_channel, log_message_thread_id

logger = logging.getLogger(__name__)

async def shorten_link_command(bot, message: types.Message):
    """
    Хендлер для команды /links.
    Принимает URL и (опционально) кастомный алиас, затем использует API для сокращения.
    """
    args = message.get_args()
    if not args:
        await message.reply("<b>Пожалуйста, укажите ссылку для сокращения.\n\nПример:</b> <code>/links https://dewinbot.ru</code>", parse_mode='HTML')
        return

    parts = args.split()
    original_url = parts[0]
    custom_alias = parts[1] if len(parts) > 1 else None # Используем None, если алиаса нет

    # Базовая проверка URL
    if not original_url.startswith('http://') and not original_url.startswith('https://'):
        await message.reply("<b>Пожалуйста, введите корректный URL (начинающийся с http:// или https://).</b>", parse_mode='HTML')
        return

    # Отправляем сообщение-заглушку и сохраняем его
    processing_message = await message.reply("<b>Сокращаю вашу ссылку, пожалуйста, подождите...</b>", parse_mode='HTML')

    api_result = await get_shortened_link(original_url, custom_alias)

    if api_result['success']:
        short_link = api_result['short_link']
        # Редактируем сообщение с результатом
        await processing_message.edit_text(f"<b>Ваша сокращенная ссылка:</b> {short_link}", parse_mode='HTML')
        await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> использовал команду <code>/links</code></b>\n"
            f"<b>💠 id пользователя: <code>{message.from_user.id}</code></b>\n\n"
            f"<b>✉️ Полученное сообщение:</b>"
            f"<b>Ваша сокращенная ссылка:</b> {short_link}",
            parse_mode="HTML", 
            message_thread_id=log_message_thread_id
            )
    else:
        error_message = api_result.get('message', '<blockquote>Неизвестная ошибка при сокращении ссылки.\n\nОбратитесь в <a href=https://t.me/DewinConferenceBot>тех. поддержку</a> или воспользуйтесь данным сервисом прямиком через <a href=https://dewinlinks.ru>наш сайт</a></blockquote>.')
        # Редактируем сообщение с ошибкой
        await processing_message.edit_text(f"<b>Произошла ошибка:</b> {error_message}", parse_mode='HTML')
