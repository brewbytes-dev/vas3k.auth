import logging

from aiogram import types, Router
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app import club
from app.club import ClubUser
from app.repos.chats import RepoChat

USER_ALREADY_PARTICIPANT = 'Bad Request: USER_ALREADY_PARTICIPANT'

logger = logging.getLogger(__name__)
router = Router(name="join_requests")


@router.chat_join_request()
async def new_join_request(request: types.ChatJoinRequest, session: AsyncSession):
    repo_chat = RepoChat(session)
    chat_entry = await repo_chat.get_or_create(request.chat.id)

    user_telegram_id = request.from_user.id
    user: ClubUser = await club.user_by_telegram_id(user_telegram_id)

    if not user or not user.approved:
        return

    if chat_entry.only_active and not user.is_active_member:
        return

    try:
        await request.approve()
    except TelegramBadRequest as e:
        if e.message != USER_ALREADY_PARTICIPANT:
            raise e
