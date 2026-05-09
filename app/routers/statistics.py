from fastapi import APIRouter
from database.database import get_platform_statistics

router = APIRouter()

@router.get("/statistics", summary="Общая статистика по платформе")
async def statistics():
    return await get_platform_statistics()