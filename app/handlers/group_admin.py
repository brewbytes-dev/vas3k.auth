import logging

from aiogram import types, Router, F
from aiogram.filters import Command, CommandObject

from aiogram.utils.markdown import hblockquote

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


@router.message(Command(commands=['entry_question']))
async def follow_up_requests(message: types.Message, command: CommandObject, repo_chat: RepoChat):
    text = None
    if command.args is None:
        current_status = await repo_chat.get_follow_up_requests_status(message.chat.id)
        if current_status is True:
            # turn off
            await repo_chat.turn_off_follow_up_requests(message.chat.id)
            await message.answer("📬 Бот больше не будет просить людей не из клуба подать заявку")
            return
    else:
        text = command.args.strip()

    # turn on with default | current text
    set_text = await repo_chat.turn_on_follow_up_requests(message.chat.id, text)
    html_text = hblockquote(set_text)

    cmd = "/entry_question"
    cmd_quote = hblockquote(f"{cmd} <новый текст>")
    await message.answer(
        f"📬✅ Бот будет просить людей не из клуба подать заявку:\n\n"
        f"{html_text}\n"
        f"\n"
        f"Текст можно изменить командой:\n"
        f"{cmd_quote}"
    )
