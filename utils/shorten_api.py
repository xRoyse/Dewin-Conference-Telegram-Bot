import logging
from aiohttp import ClientSession
from config import API_ENDPOINT 

logger = logging.getLogger(__name__)

async def get_shortened_link(original_url: str, custom_alias: str = None) -> dict:
    """
    Отправляем запрос к API сокращения ссылок и возвращает результат.

    Args:
        original_url (str): Исходный URL для сокращения.
        custom_alias (str, optional): Кастомный алиас для ссылки. Defaults to None.

    Returns:
        dict: Словарь с результатом: {'success': bool, 'message': str, 'short_link': str}
    """
    try:
        async with ClientSession() as session:
            data = {
                'url': original_url
            }
            if custom_alias:
                data['alias'] = custom_alias

            async with session.post(API_ENDPOINT, data=data) as resp:
                if resp.status != 200:
                    logger.error(f"API request failed with status: {resp.status} for URL: {original_url}")
                    return {'success': False, 'message': f"Ошибка сервера: {resp.status}"}

                api_response = await resp.json()
                return api_response

    except Exception as e:
        logger.error(f"Error communicating with API for URL {original_url}: {e}")
        return {'success': False, 'message': "Произошла внутренняя ошибка при обращении к API."}