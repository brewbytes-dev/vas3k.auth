import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.handlers.join_requests import get_or_create_new_chat

logger = logging.getLogger(__name__)

router = Router(name="group_admin")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))
router.message.filter(AdminFilter(is_admin=True))


@router.message(Command(commands=['auto_whois']))
async def show_intro(message: types.Message, session: AsyncSession):
    chat_entry, _ = await get_or_create_new_chat(message.chat.shifted_id, session)

    previous_status = chat_entry.show_intro
    switched_status = not previous_status
    if switched_status:
        await message.answer("Бот будет показывать профиль новых пользователей")
    else:
        await message.answer("Авто-whois выключен")

    chat_entry.show_intro = switched_status
    await session.commit()
