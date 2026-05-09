import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, statistics, user, group

app = FastAPI(title="Telegram Auth App", version="1.0")

# CORS — настрой под фронт
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router,prefix="/auth",tags=["Auth"])
app.include_router(statistics.router,prefix="/api",tags=["Statistics"])
app.include_router(user.router,prefix="/me",tags=["User"])
app.include_router(group.router,prefix="/groups",tags=["Group"])

# Инициализация базы при запуске
# @app.on_event("startup")
# async def startup():
#     await create_users_table()
#     await create_groups_table()
#     await create_memberships_table()
#     print("✅ Таблицы инициализированы")

# Точка входа
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
