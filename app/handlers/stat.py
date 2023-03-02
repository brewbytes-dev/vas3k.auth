import asyncio
import logging

from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.markdown import hlink
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot_loader import bot
from app.config import DEVELOPER_ID
from app.db.models import ChatEntry
from app.filters.developer import DeveloperFilter

logger = logging.getLogger(__name__)

router = Router(name="stat")
router.message.filter(F.chat.type.in_({"private"}))
router.message.filter(DeveloperFilter(is_developer=True))


@router.message(Command(commands=['stat']))
async def show_groups(message: types.Message, session: AsyncSession):
    stmt = await session.execute(
        select(ChatEntry)
    )

    chats = stmt.scalars().all()
    chat: ChatEntry
    chat_list = []
    for chat in chats:
        try:
            chat_obj = await bot.get_chat("-100" + str(chat.chat_id))
        except Exception as e:
            continue

        chat_list.append(hlink(chat_obj.title, chat_obj.invite_link))
        await asyncio.sleep(2)

    await bot.send_message(DEVELOPER_ID, "\n".join(chat_list), parse_mode=ParseMode.HTML)
