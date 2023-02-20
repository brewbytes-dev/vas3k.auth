import logging

from aiogram import types, Router
from aiogram.filters import Command

from app.loader import app_version

logger = logging.getLogger(__name__)
router = Router(name="help")


@router.message(Command(commands=['start', 'help']))
async def help_msg(message: types.Message):
    help_message = f"""
Бот для авторизации в чат через Вастрик.Клуб.
Добавьте бота в администраторы чата и включите настройку Request to join.
v{app_version} - автоапрув новых запросов в чат, если пользователь есть в клубе, остальные запросы останутся нетронутые
"""

    await message.answer(help_message)
