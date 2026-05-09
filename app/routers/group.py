
from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user, TokenUser
from database.database import get_group_info_from_db, update_welcome_message_in_db,update_farewell_message_in_db,update_banned_words_in_db,update_link_whitelist_in_db
from fastapi.exceptions import HTTPException

router = APIRouter()

@router.get("/{group_id}")
async def get_group_info(group_id: int, user: TokenUser = Depends(get_current_user)):
    group = await get_group_info_from_db(group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return group


@router.put("/{group_id}/welcome")
async def set_welcome_message(group_id: int, data: dict, user: TokenUser = Depends(get_current_user)):
    message = data.get("message", "").strip()
    if not await update_welcome_message_in_db(group_id, message):
        raise HTTPException(status_code=500, detail="Не удалось обновить сообщение")
    return {"status": "ok"}

@router.put("/{group_id}/farewell")
async def set_farewell_message(group_id: int, data: dict, user: TokenUser = Depends(get_current_user)):
    message = data.get("message", "").strip()
    success = await update_farewell_message_in_db(group_id, message)
    if not success:
        raise HTTPException(status_code=500, detail="Не удалось обновить сообщение")
    return {"status": "ok"}


@router.put("/{group_id}/banned-words")
async def set_banned_words(group_id: int, data: dict, user: TokenUser = Depends(get_current_user)):
    words = data.get("words", [])
    action = data.get("action", "")
    if not isinstance(words, list) or not isinstance(action, str):
        raise HTTPException(status_code=400, detail="Неверные данные")

    success = await update_banned_words_in_db(group_id, words, action)
    if not success:
        raise HTTPException(status_code=500, detail="Не удалось обновить настройки")
    return {"status": "ok"}

@router.put("/{group_id}/link-whitelist")
async def set_link_whitelist(group_id: int, data: dict, user: TokenUser = Depends(get_current_user)):
    links = data.get("links", [])
    action = data.get("action", "")
    if not isinstance(links, list) or not isinstance(action, str):
        raise HTTPException(status_code=400, detail="Неверные данные")

    success = await update_link_whitelist_in_db(group_id, links, action)
    if not success:
        raise HTTPException(status_code=500, detail="Не удалось обновить ссылки")
    return {"status": "ok"}