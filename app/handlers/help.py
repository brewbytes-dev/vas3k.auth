import logging

from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.markdown import hpre

from app.bot_loader import bot

logger = logging.getLogger(__name__)
router = Router(name="help")


@router.message(Command(commands=['start', 'help']))
async def help_msg(message: types.Message):
    help_message = f"""
Бот для авторизации в чат через Вастрик.Клуб [v{bot.version}].
Добавьте бота в администраторы чата и включите настройку Request admin approval.

Функционал:
Автоапрув новых запросов в чат, если пользователь есть в клубе, остальные запросы останутся нетронутые

Опции (в групповом чате):
{hpre('/auto_whois')}
    включить/отключить авто-whois участников клуба
{hpre('/only_active')}
    включить/отключить проверку действующего членства участников клуба (также бот не будет пускать забаненных)
{hpre('/entry_question <новый текст>')}
    включить/отключить заявки для людей не из клуба.
    Люди не из клуба будут получать запрос на подачу заявки с текстом, указанным в команде,
    заявка будет приходить в чат.

Вопросы и пожелания: @mindsweeper
"""

    await message.answer(help_message, parse_mode=ParseMode.HTML)
