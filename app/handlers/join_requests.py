import logging
from contextlib import suppress

from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.markdown import hlink, hpre
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app import club
from app.bot_loader import bot
from app.db.models import ChatEntry

USER_ALREADY_PARTICIPANT = 'Bad Request: USER_ALREADY_PARTICIPANT'

logger = logging.getLogger(__name__)
router = Router(name="join_requests")


@router.chat_join_request()
async def new_join_request(request: types.ChatJoinRequest, session: AsyncSession):
    chat_entry, is_new = await get_or_create_new_chat(request.chat.id, session)

    user_telegram_id = request.user_chat_id
    user = await club.user_by_telegram_id(user_telegram_id)

    if not user or not user.approved:
        return

    if chat_entry.only_active and not user.is_active_member:
        return

    try:
        await request.approve()
    except TelegramBadRequest as e:
        if e.message != USER_ALREADY_PARTICIPANT:
            raise e

    if chat_entry.show_intro or chat_entry.show_intro is None:
        intro_link = hlink(user.full_name, user.user_link)
        await bot.send_message(request.chat.id,
                               f"У нас новый участник: {intro_link}!",
                               parse_mode=ParseMode.HTML)

    # notify current chats about option
    if chat_entry.only_active is None:
        await bot.send_message(request.chat.id,
                               f"новая опция - проверка наличия актуального члентсва в клубе {hpre('/only_active')}",
                               parse_mode=ParseMode.HTML)
        chat_entry.only_active = False
        await session.commit()

    # notify current chats about option
    if chat_entry.show_intro is None:
        await bot.send_message(request.chat.id,
                               f"включить/отключить авто whois - {hpre('/auto_whois')}",
                               parse_mode=ParseMode.HTML)
        chat_entry.show_intro = True
        await session.commit()


async def get_or_create_new_chat(chat_id, session: AsyncSession):
    stmt = await session.execute(
        select(ChatEntry).where(ChatEntry.chat_id == chat_id)
    )
    is_new = False
    try:
        chat_entry: ChatEntry = stmt.scalars().one()
    except NoResultFound:
        is_new = True
        chat_entry = ChatEntry(chat_id=chat_id, show_intro=None)
        session.add(chat_entry)
        with suppress(IntegrityError):
            await session.commit()

    return chat_entry, is_new
