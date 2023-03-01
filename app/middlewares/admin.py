from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


__all__ = ['AdminMiddleware']


async def get_admin_ids(bot, chat_id):
    try:
        admins_list = await bot.get_chat_administrators(chat_id)
    except Exception:
        return None

    admins_list = [admin for admin in admins_list if not admin.user.is_bot]
    return list(set(admin.user.id for admin in admins_list))


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
        **kwargs,
    ) -> Any:

        state: FSMContext = data['state']
        state_data = await state.get_data()

        admin_ids = state_data.get("admin_ids")
        if admin_ids is None:
            bot = data['bot']
            admin_ids = await get_admin_ids(bot, event.chat.id)
            await state.update_data(admin_ids=admin_ids)

        return await handler(event, data)
