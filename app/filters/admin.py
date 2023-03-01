from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot_loader import bot
from app.middlewares.admin import get_admin_ids


class AdminFilter(BaseFilter):
    is_admin: bool

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return await user_is_admin(message, state) == self.is_admin


async def user_is_admin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    admin_ids = data.get("admin_ids")
    if admin_ids is None:
        admin_ids = await get_admin_ids(bot, message.chat.id)
        await state.update_data(admin_ids=admin_ids)

    return message.from_user.id in admin_ids
