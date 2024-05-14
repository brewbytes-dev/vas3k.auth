import html
import logging

from aiogram import types, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.markdown import hitalic, hblockquote

from app import club
from app.bot_loader import AuthBot
from app.club import ClubUser
from app.repos.chat_requests import RepoRequests
from app.repos.chats import RepoChat

USER_ALREADY_PARTICIPANT = 'Bad Request: USER_ALREADY_PARTICIPANT'

logger = logging.getLogger(__name__)
router = Router(name="join_requests")


@router.chat_join_request()
async def new_join_request(request: types.ChatJoinRequest, bot: AuthBot,
                           repo_chat: RepoChat,
                           repo_requests: RepoRequests):
    chat_entry = await repo_chat.get_or_create(request.chat.id)

    user_telegram_id = request.from_user.id
    user: ClubUser = await club.user_by_telegram_id(user_telegram_id)

    allowed = is_user_allowed(user, chat_entry.only_active)

    if allowed:
        try:
            return await request.approve()
        except TelegramBadRequest as e:
            if e.message != USER_ALREADY_PARTICIPANT:
                raise e

    if chat_entry.follow_up_requests:
        req = await repo_requests.get(request.chat.id, user_telegram_id)
        if req is not None:
            return

        chat_title = html.escape(request.chat.title)
        header = (f"✋ Привет! Ты отправил запрос в чатик \"{chat_title}\", "
                  f"но я не вижу твой телеграм аккаунт привязанным к Вастрик.Клубу.\n"
                  f"Вот что администраторы сказали мне спросить у тебя:")
        reply_info = f"Сделай \"Ответить\" на это сообщение, чтобы отправить свой ответ в чатик."
        footer = hitalic("P.S. Если ты из Клуба, но у тебя привязан другой телеграм "
                         "то добавь эту информацию в ответ!")

        request_text = await repo_chat.get_follow_up_request_text(request.chat.id)
        request_text_quote = hblockquote(request_text)

        sent_msg = await bot.send_message(request.user_chat_id,
                                          f"{header}\n\n{request_text_quote}\n\n{reply_info}\n\n{footer}"
                                          )

        await repo_requests.create(request.chat.id, user_telegram_id, sent_msg.message_id)


def is_user_allowed(user: ClubUser, check_active: bool) -> bool:
    if not user:
        return False

    if not user.approved:
        return False

    if check_active and not user.is_active_member:
        return False

    return True
