from aiogram import F, Router, Bot
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, PROMOTED_TRANSITION, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.join_requests import get_or_create_new_chat

router = Router(name="bot_in_group")
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=PROMOTED_TRANSITION
    )
)
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot, session: AsyncSession):
    chat_entry, _ = await get_or_create_new_chat(event.chat.id, session)

    await bot.send_message(
        chat_id=event.chat.id,
        text="Теперь создайте новую ссылку, включите опцию Request admin approval "
             "и бот будет автоматически принимать заявки от людей из клуба"
    )


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    )
)
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot, session: AsyncSession):
    chat_entry, _ = await get_or_create_new_chat(event.chat.id, session)

    chat_info = await bot.get_chat(event.chat.id)
    if not chat_info.permissions.can_send_messages:
        return
    await bot.send_message(
        chat_id=event.chat.id,
        text="Привет! Чтобы бот помогал администрировать чат добавь его в администраторы!"
    )


@router.message(F.migrate_to_chat_id)
async def group_to_supergroup_migration(message: Message, bot: Bot, session: AsyncSession):
    chat_entry, _ = await get_or_create_new_chat(message.chat.id, session)
    chat_entry.chat_id = message.migrate_to_chat_id
    await session.commit()
