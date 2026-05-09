from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.token import decode_jwt_token  # твоя функция расшифровки
from app.schemas.auth import TokenUser
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenUser:
    token = credentials.credentials
    try:
        payload = decode_jwt_token(token)
        return TokenUser(user_id=payload["user_id"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен или истёк"
        )