import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from app.filters.admin import AdminFilter
from app.repos.chats import RepoChat

logger = logging.getLogger(__name__)

router = Router(name="group_admin")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))
router.message.filter(AdminFilter(is_admin=True))


@router.message(Command(commands=['auto_whois']))
async def show_intro(message: types.Message, repo_chat: RepoChat):
    switched_status = await repo_chat.switch_show_intro(message.chat.id)

    if switched_status:
        await message.answer("👓✅ Бот будет показывать профиль новых пользователей")
    else:
        await message.answer("👓 Авто-whois выключен")


@router.message(Command(commands=['only_active']))
async def only_active(message: types.Message, repo_chat: RepoChat):
    switched_status = await repo_chat.switch_only_active(message.chat.id)

    if switched_status:
        await message.answer("🔒 Бот не будет пускать участников с истекшим членством")
    else:
        await message.answer("👐 Бот будет пускать всех кто был когда либо в клубе")
