from aiogram import Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, KICKED, LEFT, \
    RESTRICTED, MEMBER, ADMINISTRATOR, CREATOR
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated

router = Router(name="admin_group_changed")


def _state_admin_ids(data: dict) -> set[int]:
    return set(data.get("admin_ids") or [])


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=
        (KICKED | LEFT | RESTRICTED | MEMBER)
        >>
        (ADMINISTRATOR | CREATOR)
    )
)
async def admin_promoted(event: ChatMemberUpdated, state: FSMContext):
    data = await state.get_data()
    admin_ids = _state_admin_ids(data)
    admin_ids.add(event.new_chat_member.user.id)
    await state.update_data(admin_ids=list(admin_ids))


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=
        (KICKED | LEFT | RESTRICTED | MEMBER)
        <<
        (ADMINISTRATOR | CREATOR)
    )
)
async def admin_demoted(event: ChatMemberUpdated, state: FSMContext):
    data = await state.get_data()
    admin_ids = _state_admin_ids(data)
    admin_ids.discard(event.old_chat_member.user.id)
    await state.update_data(admin_ids=list(admin_ids))
