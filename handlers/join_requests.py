import logging

from aiogram import types, Router
from src import club

logger = logging.getLogger(__name__)
router = Router(name="join_requests")


@router.chat_join_request()
async def new_join_request(request: types.ChatJoinRequest):
    telegram_id = request.user_chat_id
    club_profile = club.parse_membership(telegram_id)

    if club_profile and club_profile.get("user"):
        return await request.approve()
