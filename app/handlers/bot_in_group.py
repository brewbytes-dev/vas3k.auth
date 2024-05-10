from aiogram import F, Router, Bot
from aiogram.enums import ParseMode
from aiogram.filters.chat_member_updated import (ChatMemberUpdatedFilter,
                                                 PROMOTED_TRANSITION,
                                                 JOIN_TRANSITION)
from aiogram.types import ChatMemberUpdated, Message
from aiogram.utils.markdown import hlink
from sqlalchemy.ext.asyncio import AsyncSession

from app import club
from app.repos.chats import RepoChat

router = Router(name="bot_in_group")
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=PROMOTED_TRANSITION
    )
)
async def bot_added_as_admin(event: ChatMemberUpdated, session: AsyncSession):
    repo_chat = RepoChat(session)
    await repo_chat.get_or_create(event.chat.id)

    await event.answer(
        text="Теперь создайте новую ссылку, включите опцию Request admin approval "
             "и бот будет автоматически принимать заявки от людей из клуба"
    )


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    )
)
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot, session: AsyncSession):
    repo_chat = RepoChat(session)
    await repo_chat.get_or_create(event.chat.id)

    chat_info = await bot.get_chat(event.chat.id)
    if not chat_info.permissions.can_send_messages:
        return

    await event.answer(
        text="Привет! Чтобы бот помогал добавь его в администраторы!"
    )


@router.message(F.migrate_to_chat_id)
async def group_to_supergroup_migration(message: Message, session: AsyncSession):
    repo_chat = RepoChat(session)
    await repo_chat.update_chat_id(message.chat.id, message.migrate_to_chat_id)


@router.chat_member(ChatMemberUpdatedFilter(
    member_status_changed=JOIN_TRANSITION
))
async def new_user_joined(event: ChatMemberUpdated, session: AsyncSession):
    repo_chat = RepoChat(session)
    chat_entry = await repo_chat.get_or_create(event.chat.id)

    if not chat_entry.show_intro:
        return

    user = await club.user_by_telegram_id(event.new_chat_member.user.id)
    if not user or not user.approved:
        return

    user_link = hlink(user.full_name, user.user_link)

    if user_link == "":
        return

    await event.answer(f"У нас новый участник: {user_link}!",
                       parse_mode=ParseMode.HTML,
                       disable_web_page_preview=True)
