import aiohttp
import logging
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher import Dispatcher
from aiogram.utils.callback_data import CallbackData

# Языки для перевода: код -> (флаг, название)
LANGUAGES = {
    "ru": ("🇷🇺", "Русский"),
    "en": ("🇺🇸", "English"),
    "es": ("🇪🇸", "Spanish"),
    "de": ("🇩🇪", "Deutsch"),
    "fr": ("🇫🇷", "Français"),
    "it": ("🇮🇹", "Italiano"),
    "tr": ("🇹🇷", "Türkçe"),
    "zh": ("🇨🇳", "中文"),
}

translate_cb = CallbackData("translate", "lang", "from_lang", "msg_id")

async def detect_language_mymemory(text):
    import re
    # Проверка на китайские символы
    if re.search('[\u4e00-\u9fff]', text):
        return "zh"
    # Проверка на кириллицу
    if re.search('[а-яА-Я]', text):
        return "ru"
    # Можно добавить другие языки по аналогии
    return "en"

async def translate_mymemory(text, from_lang, to_lang):
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={from_lang}|{to_lang}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data.get("responseData", {}).get("translatedText")

# Временное хранилище текстов для перевода
TRANSLATE_TEXTS = {}

async def translate_command_handler(message: types.Message):
    # Теперь перевод только по аргументу команды, reply игнорируется
    text = message.get_args()
    msg_id = message.message_id

    if not text:
        # Если команда вызвана как /translate\n (без аргументов), пробуем взять текст самого сообщения после команды
        if message.text:
            parts = message.text.split(maxsplit=1)
            if len(parts) > 1:
                text = parts[1]

    if not text:
        await message.reply(
            "<b>❗ Укажите текст для перевода после команды.</b>\n\n"
            "Пример: <code>/translate Hello Dewin!</code>",
            parse_mode="HTML"
        )
        return

    logging.info(f"Saving for translation: chat_id={message.chat.id}, msg_id={msg_id}, text={text[:50]}...")

    TRANSLATE_TEXTS[(message.chat.id, msg_id)] = text

    from_lang = await detect_language_mymemory(text)
    kb = InlineKeyboardMarkup(row_width=2)
    for code, (flag, name) in LANGUAGES.items():
        if code != from_lang:
            kb.insert(
                InlineKeyboardButton(
                    f"{flag} {name}",
                    callback_data=translate_cb.new(
                        lang=code,
                        from_lang=from_lang,
                        msg_id=msg_id
                    )
                )
            )
    await message.reply(
        f"<b>🌐 Определён язык:</b> <code>{LANGUAGES.get(from_lang, ('', from_lang))[1]}</code>\n"
        f"<b>Выберите язык для перевода:</b>",
        reply_markup=kb,
        parse_mode="HTML"
    )

async def translate_callback_handler(query: CallbackQuery, callback_data: dict):
    to_lang = callback_data["lang"]
    from_lang = callback_data["from_lang"]
    msg_id = int(callback_data["msg_id"])
    chat_id = query.message.chat.id

    text = TRANSLATE_TEXTS.get((chat_id, msg_id))
    logging.info(f"Getting for translation: chat_id={chat_id}, msg_id={msg_id}, text={text[:50] if text else 'None'}")

    if not text:
        await query.message.reply(
            "<b>⚠️ Не удалось получить исходный текст для перевода.</b>",
            parse_mode="HTML"
        )
        await query.answer()
        return

    translated = await translate_mymemory(text, from_lang, to_lang)
    if not translated:
        await query.message.reply(
            "<b>⚠️ Не удалось получить перевод.</b>",
            parse_mode="HTML"
        )
        await query.answer()
        return

    from_flag, from_name = LANGUAGES.get(from_lang, ("", from_lang))
    to_flag, to_name = LANGUAGES.get(to_lang, ("", to_lang))

    await query.message.reply(
        f"<b>🔄 Перевод с {from_flag} <i>{from_name}</i> на {to_flag} <i>{to_name}</i>:</b>\n\n"
        f"<b>Исходный текст:</b>\n<blockquote>{text}</blockquote>\n"
        f"<b>Перевод:</b>\n<blockquote>{translated}</blockquote>\n\n"
        f"<i>* Перевод может быть не точным.</i>",
        parse_mode="HTML"
    )
    await query.answer()

def register_translate_handlers(dp: Dispatcher):
    dp.register_message_handler(translate_command_handler, commands=['translate', 'перевести'], commands_prefix='!?./')
    dp.register_callback_query_handler(
        translate_callback_handler,
        translate_cb.filter()
    )