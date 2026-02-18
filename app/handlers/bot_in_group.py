import logging

from aiogram import F, Router, Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.chat_member_updated import (ChatMemberUpdatedFilter,
                                                 PROMOTED_TRANSITION,
                                                 JOIN_TRANSITION, ADMINISTRATOR)
from aiogram.types import ChatMemberUpdated, Message
from aiogram.utils.markdown import hlink

from app import club
from app.repos.chats import RepoChat

router = Router(name="bot_in_group")
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))
logger = logging.getLogger(__name__)

ADD_USERS_MESSAGE = ("⚠️ Чтобы бот мог добавлять пользователей, дай ему права на это "
                     "(Add members | Invite users | Добавлять пользователей | Приглашать пользователей)")


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=PROMOTED_TRANSITION
    )
)
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot, repo_chat: RepoChat):
    await repo_chat.get_or_create(event.chat.id)

    chat_info = await bot.get_chat(event.chat.id)
    if not chat_info.permissions.can_invite_users:
        return await event.answer(text=ADD_USERS_MESSAGE)

    await event.answer(
        text="⚠️ Теперь создайте новую ссылку, включите опцию Request admin approval "
             "и бот будет автоматически принимать заявки от людей из клуба"
    )


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=(ADMINISTRATOR >> ADMINISTRATOR)
    )
)
async def bot_admin_changed(event: ChatMemberUpdated):
    old = event.old_chat_member
    new = event.new_chat_member

    if not old.can_invite_users and new.can_invite_users:
        await event.answer(
            text="✅ Теперь бот может добавлять пользователей!"
        )
    elif old.can_invite_users and not new.can_invite_users:
        await event.answer(
            text="❌ Бот больше не может добавлять пользователей"
        )
    elif not new.can_invite_users:
        await event.answer(text=ADD_USERS_MESSAGE)


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    )
)
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot, repo_chat: RepoChat):
    await repo_chat.get_or_create(event.chat.id)

    chat_info = await bot.get_chat(event.chat.id)
    if not chat_info.permissions.can_send_messages:
        return

    await event.answer(
        text="✋Привет! Чтобы бот помогал добавь его в администраторы и дай права добавлять пользователей!"
    )


@router.message(F.migrate_to_chat_id)
async def group_to_supergroup_migration(message: Message, repo_chat: RepoChat):
    await repo_chat.update_chat_id(message.chat.id, message.migrate_to_chat_id)


@router.chat_member(ChatMemberUpdatedFilter(
    member_status_changed=JOIN_TRANSITION
))
async def new_user_joined(event: ChatMemberUpdated, repo_chat: RepoChat):
    chat_entry = await repo_chat.get_or_create(event.chat.id)

    if not chat_entry.show_intro:
        return

    user = await club.user_by_telegram_id(event.new_chat_member.user.id)
    if not user or not user.approved:
        return

    user_link = hlink(user.full_name, user.user_link)

    if user_link == "":
        return

    try:
        await event.answer(f"🎉 У нас новый участник: {user_link}!",
                           parse_mode=ParseMode.HTML,
                           disable_web_page_preview=True)
    except TelegramBadRequest as exc:
        if "TOPIC_CLOSED" in str(exc):
            logger.info("Skip intro message: topic is closed in chat %s", event.chat.id)
            return
        raise
