from database.database import (
    get_achievement_by_code,
    has_user_achievement,
    get_user_achievement_progress,
    set_user_achievement_progress,
    grant_user_achievement,
)

class AchievementsManager:

    @staticmethod
    async def handle_event(user_id: int, code: str, metadata: dict = {}):
        ach = await get_achievement_by_code(code)
        if not ach:
            return

        reward = ach["reward"]
        title = ach["title"]
        target = ach["target"]

        if await has_user_achievement(user_id, code):
            return

        if target is not None:
            current = await get_user_achievement_progress(user_id, code)
            increment = metadata.get("increment", 1)
            new_progress = current + increment

            if new_progress >= target:
                await grant_user_achievement(user_id, code, reward)
                await AchievementsManager._notify_user(user_id, title, reward)
            else:
                await set_user_achievement_progress(user_id, code, new_progress)
        else:
            await grant_user_achievement(user_id, code, reward)
            await AchievementsManager._notify_user(user_id, title, reward)

    @staticmethod
    async def _notify_user(user_id: int, title: str, reward: int):
        try:
            await bot.send_message(
                chat_id=user_id,
                text=(
                    f"🏆 <b>Вы получили достижение:</b> <code>{title}</code>\n"
                    f"💰 <b>Награда:</b> <code>{reward} dewin coins</code>"
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"❗ Ошибка при уведомлении пользователя {user_id}: {e}")

    @staticmethod
    async def track_progression(user_id: int, base_code: str, thresholds: list[int], metadata: dict = {}):
        """
        Обрабатывает серию прогрессивных достижений, например: 1000, 5000, 10000 сообщений.
        base_code: например, "msgs"
        thresholds: [1000, 5000, 10000, 25000]
        Достижения должны иметь code вида "msgs_1000", "msgs_5000", ...
        """
        for target in thresholds:
            full_code = f"{base_code}_{target}"
            await AchievementsManager.handle_event(user_id, full_code, metadata)
