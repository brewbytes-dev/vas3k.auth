from aiogram import F, Router, Bot, flags
from aiogram.enums import ParseMode
from aiogram.filters.chat_member_updated import (ChatMemberUpdatedFilter,
                                                 PROMOTED_TRANSITION,
                                                 JOIN_TRANSITION, ADMINISTRATOR)
from aiogram.types import ChatMemberUpdated, Message
from aiogram.utils.markdown import hlink

from app import club
from app.backend.chat import ChatBackend

router = Router(name="bot_in_group")
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))

ADD_USERS_MESSAGE = ("⚠️ Чтобы бот мог добавлять пользователей, дай ему права на это "
                     "(Add members | Invite users | Добавлять пользователей | Приглашать пользователей)")


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=PROMOTED_TRANSITION
    )
)
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot, chat_backend: ChatBackend):
    await chat_backend.get_or_create(event.chat.id)

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


@flags.release_notes
@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    )
)
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot, chat_backend: ChatBackend):
    await chat_backend.get_or_create(event.chat.id)

    chat_info = await bot.get_chat(event.chat.id)
    if not chat_info.permissions.can_send_messages:
        return

    await event.answer(
        text="✋Привет! Чтобы бот помогал добавь его в администраторы и дай права добавлять пользователей!"
    )


@flags.release_notes
@router.message(F.migrate_to_chat_id)
async def group_to_supergroup_migration(message: Message, chat_backend: ChatBackend):
    await chat_backend.update_chat_id(message.chat.id, message.migrate_to_chat_id)


@flags.release_notes
@router.chat_member(ChatMemberUpdatedFilter(
    member_status_changed=JOIN_TRANSITION
))
async def new_user_joined(event: ChatMemberUpdated, chat_backend: ChatBackend):
    chat_entry = await chat_backend.get_or_create(event.chat.id)

    if not chat_entry.show_intro:
        return

    user = await club.user_by_telegram_id(event.new_chat_member.user.id)
    if not user or not user.approved:
        return

    user_link = hlink(user.full_name, user.user_link)

    if user_link == "":
        return

    await event.answer(f"🎉 У нас новый участник: {user_link}!",
                       parse_mode=ParseMode.HTML,
                       disable_web_page_preview=True)
