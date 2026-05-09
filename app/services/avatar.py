
import aiohttp
import os


async def download_avatar(bot, user_id):
    # Получаем аватар пользователя
    photos = await bot.get_user_profile_photos(user_id, limit=1)
    if photos.total_count == 0:
        return None  # У пользователя нет аватарки

    # Берем самое большое изображение из первой фотки
    largest_photo = photos.photos[0][-1]  # Последний элемент — самый большой
    file = await bot.get_file(largest_photo.file_id)

    # Скачиваем по прямому URL
    file_path = file.file_path
    url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'

    save_dir = '/Users/axeka/Downloads/DewinBot (dev.)/media/avatars'
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f'{user_id}.jpg')

    # Сохраняем файл
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await resp.read())

    return save_path  # Возвращаем путь к файлу
