import aiohttp
import random
import re
from aiogram import types, Bot
from aiogram.types import InputMediaPhoto

# Импортируем bot из config
from config import cfg, bot
from utils.loader import dew_channel, log_message_thread_id

# Возвращаем devid из конфига
devid = cfg['dev_id']

async def detect_language_mymemory(text):
    if re.search('[\u4e00-\u9fff]', text):
        return "zh"
    if re.search('[а-яА-Я]', text):
        return "ru"
    return "en"

async def translate_mymemory(text, from_lang, to_lang):
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={from_lang}|{to_lang}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                if data.get("responseStatus") != 200:
                    print(f"Ошибка MyMemory API: {data.get('responseDetails', 'Неизвестно')}")
                    return None
                return data.get("responseData", {}).get("translatedText")
        except aiohttp.ClientError as e:
            print(f"Ошибка при запросе к MyMemory API: {e}")
            return None
        except Exception as e:
            print(f"Неизвестная ошибка при переводе MyMemory: {e}")
            return None


async def get_meme_from_imgflip():
    """Получает случайный мем с Imgflip API"""
    url = "https://api.imgflip.com/get_memes"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                
                if not data.get('success'):
                    return None, "Ошибка Imgflip API"
                
                memes = data.get('data', {}).get('memes', [])
                if not memes:
                    return None, "Нет доступных мемов"
                
                # Выбираем случайный мем
                chosen_meme = random.choice(memes)
                return chosen_meme['url'], chosen_meme['name']
                
        except aiohttp.ClientError as e:
            return None, f"Ошибка при запросе к Imgflip: {e}"
        except Exception as e:
            return None, f"Неизвестная ошибка Imgflip: {type(e).__name__}: {e}"


async def get_meme_from_meme_api():
    """Получает случайный мем с meme-api.com"""
    url = "https://meme-api.com/gimme"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                
                # Проверяем, что это изображение, а не видео
                if data.get('spoiler') or data.get('nsfw'):
                    return None, "Неподходящий контент"
                
                url_image = data.get('url')
                title = data.get('title', 'Мем')
                
                if not url_image:
                    return None, "Нет URL изображения"
                
                return url_image, title
                
        except aiohttp.ClientError as e:
            return None, f"Ошибка при запросе к meme-api: {e}"
        except Exception as e:
            return None, f"Неизвестная ошибка meme-api: {type(e).__name__}: {e}"


async def get_meme_from_apileague(lang="en"):
    """Получает случайный мем с API League"""
    # Это требует API ключ, но дает бесплатную квоту
    url = "https://api.apileague.com/retrieve-random-meme"
    params = {
        'max-age-days': 365,  # Мемы не старше года
    }
    
    # Если у вас есть API ключ от apileague.com, добавьте его в headers
    headers = {
        'x-api-key': '3b7a9b231d244cacb5d0a04ed9c79d16'
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, headers=headers) as resp:
                if resp.status == 401:
                    return None, "Требуется API ключ для apileague.com"
                
                resp.raise_for_status()
                data = await resp.json()
                
                url_image = data.get('url')
                description = data.get('description', 'Случайный мем')
                
                if not url_image:
                    return None, "Нет URL изображения"
                
                return url_image, description
                
        except aiohttp.ClientError as e:
            return None, f"Ошибка при запросе к apileague: {e}"
        except Exception as e:
            return None, f"Неизвестная ошибка apileague: {type(e).__name__}: {e}"


async def get_russian_memes_from_reddit():
    """Получает мемы с русскоязычных сабреддитов"""
    russian_subreddits = ['Pikabu', 'russiamemes', 'Russian', 'russia']
    chosen_subreddit = random.choice(russian_subreddits)
    
    url = f"https://www.reddit.com/r/{chosen_subreddit}/hot.json?limit=25"
    
    headers = {
        'User-Agent': 'TelegramBot/1.0 (Contact: example@email.com)'
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                data = await resp.json()
                
                posts = data.get('data', {}).get('children', [])
                image_posts = []
                
                for post in posts:
                    post_data = post.get('data', {})
                    url_img = post_data.get('url', '')
                    title = post_data.get('title', '')
                    
                    # Проверяем, что это изображение
                    if (url_img.endswith(('.jpg', '.jpeg', '.png', '.gif')) or 
                        'i.redd.it' in url_img or 'i.imgur.com' in url_img):
                        
                        if not post_data.get('over_18', False):  # Не NSFW
                            # Проверяем язык заголовка - добавляем только русские или переводимые
                            detected_lang = await detect_language_mymemory(title)
                            if detected_lang == "ru" or len(title.strip()) == 0:
                                image_posts.append({
                                    'url': url_img,
                                    'title': title if title.strip() else 'Русский мем'
                                })
                
                if not image_posts:
                    return None, "Не найдено подходящих русских мемов"
                
                chosen_post = random.choice(image_posts)
                return chosen_post['url'], chosen_post['title']
                
        except aiohttp.ClientError as e:
            return None, f"Ошибка при запросе к Reddit: {e}"
        except Exception as e:
            return None, f"Неизвестная ошибка Reddit: {type(e).__name__}: {e}"


async def get_english_memes_from_reddit():
    """Получает мемы с англоязычных сабреддитов"""
    english_subreddits = ['memes', 'dankmemes', 'wholesomememes', 'funny', 'MemeEconomy']
    chosen_subreddit = random.choice(english_subreddits)
    
    url = f"https://www.reddit.com/r/{chosen_subreddit}/hot.json?limit=25"
    
    headers = {
        'User-Agent': 'TelegramBot/1.0 (Contact: example@email.com)'
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                data = await resp.json()
                
                posts = data.get('data', {}).get('children', [])
                image_posts = []
                
                for post in posts:
                    post_data = post.get('data', {})
                    url_img = post_data.get('url', '')
                    title = post_data.get('title', '')
                    
                    # Проверяем, что это изображение
                    if (url_img.endswith(('.jpg', '.jpeg', '.png', '.gif')) or 
                        'i.redd.it' in url_img or 'i.imgur.com' in url_img):
                        
                        if not post_data.get('over_18', False):  # Не NSFW
                            image_posts.append({
                                'url': url_img,
                                'title': title if title.strip() else 'English meme'
                            })
                
                if not image_posts:
                    return None, "Не найдено подходящих английских мемов"
                
                chosen_post = random.choice(image_posts)
                return chosen_post['url'], chosen_post['title']
                
        except aiohttp.ClientError as e:
            return None, f"Ошибка при запросе к Reddit: {e}"
        except Exception as e:
            return None, f"Неизвестная ошибка Reddit: {type(e).__name__}: {e}"


async def get_random_meme(lang="ru"):
    """
    Получает случайный мем в зависимости от выбранного языка
    """
    if lang == "ru":
        # Для русского языка используем только русские источники
        sources = [
            get_russian_memes_from_reddit,
        ]
        
        # Добавляем универсальные источники с фильтрацией
        universal_sources = [
            get_meme_from_imgflip,
            get_meme_from_apileague
        ]
        
        # Сначала пробуем русские источники
        random.shuffle(sources)
        for source_func in sources:
            try:
                meme_url, meme_title = await source_func()
                if meme_url:
                    return meme_url, meme_title
            except Exception as e:
                print(f"Ошибка в русском источнике {source_func.__name__}: {e}")
                continue
        
        # Если русские источники не сработали, пробуем универсальные с переводом
        random.shuffle(universal_sources)
        for source_func in universal_sources:
            try:
                if source_func == get_meme_from_apileague:
                    meme_url, meme_title = await source_func(lang)
                else:
                    meme_url, meme_title = await source_func()
                
                if meme_url:
                    # Проверяем язык заголовка и переводим если нужно
                    detected_lang = await detect_language_mymemory(meme_title)
                    if detected_lang == "en":
                        translated_title = await translate_mymemory(meme_title, "en", "ru")
                        if translated_title:
                            return meme_url, f"{meme_title}|{translated_title}"
                    return meme_url, meme_title
                    
            except Exception as e:
                print(f"Ошибка в универсальном источнике {source_func.__name__}: {e}")
                continue
    
    else:  # lang == "en"
        # Для английского языка используем англоязычные источники
        sources = [
            get_english_memes_from_reddit,
            get_meme_from_meme_api,
            get_meme_from_imgflip,
            get_meme_from_apileague
        ]
        
        random.shuffle(sources)
        
        for source_func in sources:
            try:
                if source_func == get_meme_from_apileague:
                    meme_url, meme_title = await source_func(lang)
                else:
                    meme_url, meme_title = await source_func()
                
                if meme_url:
                    return meme_url, meme_title
                    
            except Exception as e:
                print(f"Ошибка в английском источнике {source_func.__name__}: {e}")
                continue
    
    # Если все источники не сработали
    return None, "Все источники мемов недоступны. Попробуйте позже."


async def send_meme(bot_instance: Bot, message_to_edit: types.Message, lang: str, user_id: int, user_username: str, chat_title: str, chat_id: int):
    """
    Получает и отправляет мем, редактируя существующее сообщение.
    Возвращает True в случае успеха, False в случае ошибки.
    """
    try:
        meme_url, meme_title = await get_random_meme(lang)
        if not meme_url:
            # Пользователю показываем ТОЛЬКО стандартное сообщение об ошибке.
            await message_to_edit.edit_text("Ой... Похоже у нас проблемки... Команда разработчиков уже уведомлена!")

            # Отправляем подробную ошибку разработчику
            if devid:
                error_message_for_dev = (
                    f"🚨 Ошибка в команде /mems (от get_random_meme)!\n"
                    f"Причина: <code>{meme_title}</code>\n"
                    f"Пользователь: @{user_username} (ID: <code>{user_id}</code>)\n"
                    f"Группа: <code>{chat_title}</code> (ID: <code>{chat_id}</code>)"
                )
                await bot_instance.send_message(devid, error_message_for_dev, parse_mode='HTML')
            return False

        caption = ""
        
        # Проверяем, есть ли разделитель для перевода
        if "|" in meme_title:
            original_title, translated_title = meme_title.split("|", 1)
            caption = (
                f"<b>{original_title}</b>\n"
                f"✩ ───   💙  ─── ✩\n"
                f"<b>{translated_title}</b>\n\n"
                f"<i>Перевод был выполнен с помощью /translate и может быть не точным.</i>"
            )
        elif lang == "en":
            # Для английских мемов пытаемся перевести
            translated_title = await translate_mymemory(meme_title, "en", "ru")
            if translated_title:
                caption = (
                    f"<b>{meme_title}</b>\n"
                    f"✩ ───   💙  ─── ✩\n"
                    f"<b>{translated_title}</b>\n\n"
                    f"<i>Перевод был выполнен с помощью /translate и может быть не точным.</i>"
                )
            else:
                caption = f"<b>{meme_title}</b>"
                if devid:
                    error_message_for_dev = (
                        f"⚠️ Предупреждение: Не удалось перевести мем для пользователя!\n"
                        f"Оригинальный заголовок: <code>{meme_title}</code>\n"
                        f"Пользователь: @{user_username} (ID: <code>{user_id}</code>)\n"
                        f"Группа: <code>{chat_title}</code> (ID: <code>{chat_id}</code>)"
                    )
                    await bot_instance.send_message(devid, error_message_for_dev, parse_mode='HTML')
        else:  # lang == "ru"
            # Для русских мемов просто показываем заголовок
            caption = f"<b>{meme_title}</b>"

        media = InputMediaPhoto(media=meme_url, caption=caption, parse_mode='HTML')
        await message_to_edit.edit_media(media)

        # --- Логирование успешной отправки мема ---
        try:
            await bot_instance.send_photo(
                dew_channel,
                meme_url,
                caption=(
                    f"<b>👥  Группа: <code>{chat_title}</code></b>\n\n"
                    f"<b>👤 Пользователь <a href='tg://user?id={user_id}'>{user_username}</a> использовал команду <code>/mems</code></b>\n"
                    f"<b>✉️ Полученное сообщение:</b>\n"
                    f"<blockquote>{caption}</blockquote>\n\n"
                    f"<b>💠 id пользователя: <code>{user_id}</code></b>\n"
                ),
                parse_mode="HTML",
                message_thread_id=log_message_thread_id
            )
        except Exception as log_e:
            if devid:
                await bot_instance.send_message(
                    devid,
                    f"⚠️ Не удалось залогировать мем в dew_channel: <code>{type(log_e).__name__}: {log_e}</code>",
                    parse_mode="HTML"
                )


        return True
    except Exception as e:
        # Всегда выводим пользователю стандартное сообщение
        try:
            await message_to_edit.edit_text("Ой... Похоже у нас проблемки... Команда разработчиков уже уведомлена!")
        except Exception as edit_e:
            # Если даже это не удалось, отправляем новое сообщение
            await bot_instance.send_message(message_to_edit.chat.id, "Ой... Похоже у нас проблемки... Команда разработчиков уже уведомлена!")

        # Всегда отправляем детальное сообщение об ошибке разработчику
        if devid:
            error_message_for_dev = (
                f"🚨 Критическая ошибка в send_meme!\n"
                f"Причина: <code>{type(e).__name__}: {e}</code>\n"
                f"Пользователь: @{user_username} (ID: <code>{user_id}</code>)\n"
                f"Группа: <code>{chat_title}</code> (ID: <code>{chat_id}</code>)"
            )
            await bot_instance.send_message(devid, error_message_for_dev, parse_mode='HTML')
        return False


async def mems_command_handler(message: types.Message):
    """Обработчик команды /mems"""
    try:
        # Отправляем сообщение о поиске мема
        loading_message = await message.reply("🔍 Ищу крутой мем...")
        
        # Получаем данные пользователя и чата
        user_username = message.from_user.username if message.from_user.username else "N/A"
        chat_title = message.chat.title if message.chat.title else "Личный чат"
        
        # Сразу отправляем русский мем
        success = await send_meme(
            bot, 
            loading_message, 
            "ru", 
            message.from_user.id, 
            user_username, 
            chat_title, 
            message.chat.id
        )

    except Exception as e:
        await message.reply("Ой... Похоже у нас проблемки... Команда разработчиков уже уведомлена!")
        if devid:
            user_username = message.from_user.username if message.from_user.username else "N/A"
            chat_title = message.chat.title if message.chat.title else "Личный чат"
            error_message_for_dev = (
                f"🚨 Ошибка в mems_command_handler!\n"
                f"Причина: <code>{type(e).__name__}: {e}</code>\n"
                f"Пользователь: @{user_username} (ID: <code>{message.from_user.id}</code>)\n"
                f"Группа: <code>{chat_title}</code> (ID: <code>{message.chat.id}</code>)"
            )
            await bot.send_message(devid, error_message_for_dev, parse_mode='HTML')