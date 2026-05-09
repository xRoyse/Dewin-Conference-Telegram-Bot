from aiogram import types
from database.database import get_reputation, update_reputation
from utils.loader import dew_channel, log_message_thread_id
from utils.operators import handlers_commands
from collections import defaultdict
import time

reputation_limits = defaultdict(lambda: {'count': 0, 'last_reset': time.time()})

async def reputation_message_handler(bot, message: types.Message):
    if not message.reply_to_message:
        return  # Если нет ответа на сообщение, ничего не делаем

    replied_user_id = message.reply_to_message.from_user.id
    group_id = message.chat.id

    message_words = message.text.lower().split()
    if not message_words:
        return  
    
    if message.from_user.id == 7803753519:
        return  
    
    # Проверяем, не является ли пользователь тем, на кого отвечает
    if message.from_user.id == replied_user_id:
        return  # Не отправляем сообщение, просто выходим из функции

    first_word = message_words[0]
    trigger_words_positive = ["топ", "харош", "+", "лучший", "плюсую", "молодец", "спасибо", "спс", "пасибо", "респект", "плюс", "огонь", "имба"]
    trigger_words_negative = ["плох", "пидр", "гандон", "диз"]

    action = None
    if first_word in trigger_words_positive:
        action = 1
    elif first_word in trigger_words_negative:
        action = -1

    if action is not None:
        current_time = time.time()
        user_key = (group_id, replied_user_id)

        if current_time - reputation_limits[user_key]['last_reset'] >= 86400:  
            reputation_limits[user_key]['count'] = 0
            reputation_limits[user_key]['last_reset'] = current_time

        if reputation_limits[user_key]['count'] >= 5:
            await message.answer("<b>⚠️ Вы уже достигли лимита начислений/уменьшений репутации для этого пользователя на сегодня.</b>", parse_mode='html')
            return

        reputation_limits[user_key]['count'] += 1

        current_reputation = await get_reputation(group_id, replied_user_id)
        new_reputation = current_reputation + action

        await update_reputation(group_id, replied_user_id, action)

        action_text = "увеличена" if action == 1 else "уменьшена"
        emoji = "✅" if action == 1 else "🛑"

        await message.answer(
            f"<b>{emoji} Репутация пользователя <a href='tg://user?id={replied_user_id}'>{message.reply_to_message.from_user.first_name}</a> {action_text} на <code>1</code>! <blockquote>Теперь его репутация: {new_reputation}.</blockquote></b>",
            parse_mode='html'
        )
        await bot.send_message(
            dew_channel, 
            f"<b>👥  Группа: <code>{message.chat.title}</code></b>\n\n"
            f"<b>👤 Пользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> {action_text} репутацию <a href='tg://user?id={replied_user_id}'>{message.reply_to_message.from_user.first_name}</a> <blockquote>Теперь его репутация: {new_reputation}.</blockquote></b>\n"
            f"<b>💠 id пользователей: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> <code>({message.from_user.id})</code> & <a href='tg://user?id={replied_user_id}'>{message.reply_to_message.from_user.first_name}</a> <code>({replied_user_id})</code></b>\n\n",
            parse_mode="HTML", message_thread_id=log_message_thread_id
        )
    else: 
        await handlers_commands(bot, message)
