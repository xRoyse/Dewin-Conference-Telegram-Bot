import aiohttp
from aiogram import types
from config import OWM_API_KEY

async def weather_command_handler(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply(
            "<b>❗ Пожалуйста, укажите город.</b>\n\n"
            "Пример: <code>/weather Москва</code>",
            parse_mode="HTML"
        )
        return

    city = args.strip()
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OWM_API_KEY}&units=metric&lang=ru"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 404:
                    await message.reply(
                        "<b>❗ Город не найден.</b>\n"
                        "Проверьте правильность написания.",
                        parse_mode="HTML"
                    )
                    return
                if resp.status != 200:
                    error_text = await resp.text()
                    await message.reply(
                        f"<b>⚠️ Ошибка при получении данных с погодного сервиса.</b>\n"
                        f"<b>Код:</b> <code>{resp.status}</code>\n"
                        f"<b>Ответ:</b> <code>{error_text}</code>",
                        parse_mode="HTML"
                    )
                    return
                data = await resp.json()
    except Exception:
        await message.reply(
            "<b>⚠️ Произошла ошибка при обращении к погодному сервису.</b>",
            parse_mode="HTML"
        )
        return

    try:
        temp = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description'].capitalize()
        city_name = data['name']

        weather_message = (
            f"<b>🏣 Погода в городе <b>{city_name}</b>:</b>\n\n"
            f"<blockquote>🌡 <b>Температура:</b> <code>{temp}°C</code>\n"
            f"🤗 <b>Ощущается как:</b> <code>{feels_like}°C</code>\n"
            f"💧 <b>Влажность:</b> <code>{humidity}%</code>\n"
            f"💨 <b>Ветер:</b> <code>{wind_speed} м/с</code>\n"
            f"📝 <b>Описание:</b> <i>{description}</i></blockquote>"
        )
        await message.reply(weather_message, parse_mode="HTML")
    except Exception:
        await message.reply(
            "<b>⚠️ Не удалось обработать данные о погоде.</b>",
            parse_mode="HTML"
        )