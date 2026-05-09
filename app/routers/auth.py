from fastapi import APIRouter, HTTPException, Request
from app.schemas.auth import TelegramAuthData
from app.auth.token import check_telegram_auth, create_jwt_token
# from app.crud.users import upsert_user
from app.core.logger import logger
from database.database import upsert_user
import time

router = APIRouter()


@router.post("/telegram", summary="Авторизация через Telegram")
async def telegram_auth(payload: TelegramAuthData, request: Request):
    """
    Обработка авторизации через Telegram Widget.
    """
    user_data = payload.dict()
    logger.info(f"[Auth] Попытка входа от Telegram-пользователя {user_data.get('id')}")

    if not check_telegram_auth(user_data.copy()):
        logger.warning("[Auth] Проверка Telegram-подписи не пройдена")
        raise HTTPException(status_code=403, detail="Неверные данные Telegram")

    if time.time() - payload.auth_date > 86400:
        logger.warning("[Auth] Данные Telegram устарели")
        raise HTTPException(status_code=403, detail="Данные Telegram устарели")

    await upsert_user(payload.id, payload.username, None)

    token = create_jwt_token(payload.id)
    logger.info(f"[Auth] Пользователь {payload.id} авторизован")

    return {"access_token": token, "token_type": "bearer", "user_id": payload.id}
