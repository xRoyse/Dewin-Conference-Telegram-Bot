import hashlib
import hmac
import jwt
from datetime import datetime, timedelta
from jwt import ExpiredSignatureError, InvalidTokenError
from app.core.config import BOT_TOKEN, JWT_SECRET, JWT_ALGORITHM
from fastapi import HTTPException, status


def check_telegram_auth(data: dict) -> bool:
    data = data.copy()
    hash_check = data.pop("hash", None)
    if not hash_check:
        print("❌ Hash отсутствует")
        return False

    cleaned_data = {
        k: v for k, v in data.items()
        if v is not None
    }

    # Строим data_check_string
    data_check_string = '\n'.join(
        f"{k}={v}" for k, v in sorted(cleaned_data.items())
    )

    print("🔍 Data check string:\n", data_check_string)

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    print("🧮 Вычисленный HMAC hash:", hmac_hash)
    print("📨 Полученный hash от Telegram:", hash_check)

    result = hmac.compare_digest(hmac_hash, hash_check)
    print("✅ Совпадают?" if result else "❌ Не совпадают")

    return result


def create_jwt_token(user_id: int) -> str:
    """Создаёт JWT токен для авторизованного пользователя"""
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=1),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str) -> dict:
    """
    Декодирует JWT и возвращает словарь с user_id, взятым из поля `sub`.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
        return {"user_id": user_id}
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истёк"
        )
    except (InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен"
        )