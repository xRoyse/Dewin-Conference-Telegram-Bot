from fastapi import APIRouter, Depends
from app.schemas.settings import GroupSettingsUpdate, GroupSettingsResponse

from app.auth.dependencies import get_current_user, TokenUser
from database.database import get_user_profile, get_user_groups, get_owned_groups, get_total_messages, \
    get_user_group_settings, apply_group_settings_update, get_full_achievement_status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/", summary="Профиль текущего пользователя")
async def me(user: TokenUser = Depends(get_current_user)):
    data = await get_user_profile(user.user_id)
    if not data:
        return JSONResponse(status_code=404, content={"detail": "Пользователь не найден"})
    return data


@router.get("/groups", summary="Группы, в которых пользователь состоит")
async def user_groups(user: TokenUser = Depends(get_current_user)):
    return await get_user_groups(user.user_id)


@router.get("/owned-groups", summary="Группы, где пользователь — основатель")
async def user_owned_groups(user: TokenUser = Depends(get_current_user)):
    return await get_owned_groups(user.user_id)


@router.get("/messages", summary="Общее число сообщений пользователя")
async def user_messages(user: TokenUser = Depends(get_current_user)):
    return await get_total_messages(user.user_id)


@router.get("/group-settings", response_model=GroupSettingsResponse)
async def get_all_group_settings(user: TokenUser = Depends(get_current_user)):
    return await get_user_group_settings(user.user_id)


@router.post("/group-settings/update")
async def update_group_settings(data: GroupSettingsUpdate, user: TokenUser = Depends(get_current_user)):
    success = await apply_group_settings_update(user.user_id, data)
    if not success:
        return JSONResponse(status_code=403, content={"detail": "Нет доступа или группа не найдена"})
    return {"status": "ok"}


@router.get("/achievements")
async def user_achievements(user: TokenUser = Depends(get_current_user)):
    data = await get_full_achievement_status(user.user_id)
    total = len(data)
    completed = sum(1 for a in data if a["completed"])
    percent = int((completed / total) * 100)

    return {
        "total": total,
        "completed": completed,
        "percent": percent,
        "achievements": data
    }
