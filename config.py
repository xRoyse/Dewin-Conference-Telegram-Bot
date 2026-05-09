import os
from aiogram import Bot

TOKEN = 'TOKEN'
OWM_API_KEY = '427f3824a186f108c8fdd6f986ed0878'
CHANNEL_ID = 'ID' #ид канала для отправки различных сообщений от имени бота
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///support_tickets.db")
ADMIN_CHAT_ID = os.getenv("0000000000", "-1000000000000/4") #ид админа, ид канала для отправки логов (в данном случае в 4 чат суппер-группы)
API_ENDPOINT = 'https://dewinbot.ru/api/shorten.php'
DEVELOPER = 1302525645

bot = Bot(token=TOKEN)

"""
Пути к GIF для команд
"""
GIF_BOOP = "media/gif/boop/"
GIF_COMPLIMENT = "media/gif/compliment/"
GIF_DANCE = "media/gif/dance/"
GIF_HANDSHAKE = "media/gif/handshake/"
GIF_HEADPAT = "media/gif/headpat/"
GIF_HIGHFIVE = "media/gif/highfive/"
GIF_HIT = "media/gif/hit/"
GIF_HUG = "media/gif/hug/"
GIF_KISS = "media/gif/kiss/"
GIF_LOVE = "media/gif/love/"
GIF_SLAP = "media/gif/slap/"
GIF_WAVE = "media/gif/wave/"
GIF_WISHLUCK = "media/gif/wishluck/"
GIF_GOOD_MORNING = "media/gif/good_morning/"
GIF_GOOD_NIGHT = "media/gif/good_night/"

"""
Конфиг для саппорт части
"""
cfg = {
	'token': 'TOKEN', #
	'name': 'Dewin » ConferenceBot', #
	'dev_id': 0000000000, #id разработчика
	'teh_chat_id': -1000000000000, #id чата для вывода сообщений из саппорт бота
	'db_url': 'mongodb+srv://...', #Ссылка на БД
	'db_name': 'Dewin-Support', #Имя БД

	'button_new_question': '✉ Задать вопрос',
	'button_back': '◀️ Назад',

	'welcome_message': 'Приветствуем вас! Вы были перенаправлены в *техническую поддержку*! 🛠',
	'error_message': 'Упс! *Ошибка!* Не переживайте, ошибка уже *отправлена* разработчику.\n\nЕсли у вас срочный вопрос, вы можете написать разработчику на прямую -> @xRoyse',
	'ban_message': '⚠ Вы *забанены* в боте!',
	'question_type_ur_question_message': '📝 Введите ваш вопрос (Можно прикрепить фото):',
	'question_ur_question_sended_message': '✉ Ваш вопрос был отослан! Ожидайте ответа от тех.поддержки.',

	'1lvl_adm_name': 'Агент Поддержки',
	'2lvl_adm_name': 'Администратор',
	'3lvl_adm_name': 'Руководитель Проекта'
}

"""
Заготовки под отчивки (не реализовано)
"""
ACHIEVEMENTS = [
    {
        "code": "first_group",
        "title": "Первая встреча",
        "description": "Пригласи бота в группу",
        "reward": 10,
        "target": None,
        "event": "group_created"
    },
    {
        "code": "msgs_1000",
        "title": "Мал, но удал",
        "description": "Напиши 1000 сообщений в группах с ботом",
        "reward": 20,
        "target": 1000,
        "event": "message_sent"
    },
    {
        "code": "msgs_5000",
        "title": "Активный собеседник",
        "description": "Напиши 5000 сообщений в группах с ботом",
        "reward": 50,
        "target": 5000,
        "event": "message_sent"
    },
    {
        "code": "msgs_10000",
        "title": "Мастер словесности",
        "description": "Напиши 10000 сообщений в группах с ботом",
        "reward": 100,
        "target": 10000,
        "event": "message_sent"
    },
    {
        "code": "msgs_25000",
        "title": "Легенда чатов",
        "description": "Напиши 25000 сообщений в группах с ботом",
        "reward": 250,
        "target": 25000,
        "event": "message_sent"
    },
    {
        "code": "admin_promote",
        "title": "Доверие = сила",
        "description": "Повысь уровень администрирования в группе другому пользователю",
        "reward": 15,
        "target": None,
        "event": "admin_promoted"
    },
    {
        "code": "mute_user",
        "title": "Мьют - как искусство",
        "description": "Замьють пользователя в группе",
        "reward": 15,
        "target": None,
        "event": "user_muted"
    },
    {
        "code": "ban_user",
        "title": "Изгнание грешника",
        "description": "Забань пользователя в группе",
        "reward": 20,
        "target": None,
        "event": "user_banned"
    },
    {
        "code": "buy_subscription",
        "title": "Новые возможности!",
        "description": "Купи платный доступ бота (Подписку)",
        "reward": 100,
        "target": None,
        "event": "subscription_bought"
    },
    {
        "code": "admin_demote",
        "title": "Обратный билет",
        "description": "Понизь уровень администрирования в группе другому пользователю",
        "reward": 10,
        "target": None,
        "event": "admin_demoted"
    },
    {
        "code": "filters_on",
        "title": "Чат в безопасности!",
        "description": "Включить антиспам и другие фильтры в группе",
        "reward": 15,
        "target": None,
        "event": "filters_enabled"
    },
    {
        "code": "rep_25",
        "title": "Уважение - сила!",
        "description": "Набери 25 репутации в группе",
        "reward": 20,
        "target": 25,
        "event": "reputation_changed"
    },
    {
        "code": "rep_minus_10",
        "title": "Не любимчик",
        "description": "Набери -10 репутации в группе",
        "reward": 10,
        "target": -10,
        "event": "reputation_changed"
    },
    {
        "code": "married",
        "title": "Судьба свела в чате",
        "description": "Заключи бракосочетание в группе",
        "reward": 30,
        "target": None,
        "event": "married"
    },
    {
        "code": "divorced",
        "title": "Свободен как ветер",
        "description": "Расторгни брачный договор в группе",
        "reward": 20,
        "target": None,
        "event": "divorced"
    },
    {
        "code": "send_sms",
        "title": "Мегафон в руках",
        "description": "Отправь уведомление всем пользователям в ЛС",
        "reward": 10,
        "target": None,
        "event": "sms_sent"
    },
    {
        "code": "mention_all",
        "title": "Внимание, собрание!",
        "description": "Упомяни всех пользователей в группе",
        "reward": 10,
        "target": None,
        "event": "all_mentioned"
    },
    {
        "code": "fun_command",
        "title": "Долой рутину!",
        "description": "Используй развлекательные команды в группе",
        "reward": 5,
        "target": None,
        "event": "fun_command_used"
    },
    {
        "code": "send_report",
        "title": "Появился вопрос? Не проблема!",
        "description": "Отправь запрос в техподдержку через ЛС бота",
        "reward": 10,
        "target": None,
        "event": "report_sent"
    },
    {
        "code": "quit_chat",
        "title": "Сбежал с помощью бота",
        "description": "Выйти из беседы с помощью бота",
        "reward": 10,
        "target": None,
        "event": "quit_chat"
    }
]

ICON_MAP = {
    "msgs_1000": "01.svg",
    "msgs_5000": "06.svg",
    "ban_user": "04.svg",
    "married": "07.svg",
}
