from aiogram import F, Router, flags
from aiogram.types import Message
from aiogram.utils.markdown import hblockquote, hitalic

from app.backend.chat import ChatBackend
from app.bot_loader import AuthBot

router = Router(name="private")
router.my_chat_member.filter(F.chat.type.in_({"private"}))


@flags.release_notes
@router.message(F.reply_to_message & F.text)
async def reply_to_message(message: Message, bot: AuthBot, chat_backend: ChatBackend):
    if message.reply_to_message.from_user.id != (await message.bot.me()).id:
        return

    req = await chat_backend.get_request_by_message_id(message.from_user.id,
                                                       message.reply_to_message.message_id)

    if req is None:
        return await bot.send_message(
            message.from_user.id,
            "📬 Не понял вас. Если хотите отправить запрос в чат, ответьте на нужное сообщение бота",
            reply_to_message_id=message.message_id,
            allow_sending_without_reply=True)

    if req.sent:
        return await bot.send_message(
            message.from_user.id,
            "📬 Ваше сообщение уже отправлено",
            reply_to_message_id=req.sent_message_id,
            allow_sending_without_reply=True)

    await chat_backend.mark_request_as_sent(req.req_id, message.message_id)

    header = f"📬 Запрос в чат от {message.from_user.mention_html()}:"
    msg_quote = hblockquote(message.text)
    footer = hitalic("Примите заявку, если запрос нравится")

    await bot.send_message(
        req.chat_id,
        f"{header}\n\n{msg_quote}\n\n{footer}"
    )

    await bot.send_message(
        message.from_user.id,
        "📬 Ваш запрос отправлен, вас добавят в чат если администраторы его одобрят",
        reply_to_message_id=message.message_id,
        allow_sending_without_reply=True
    )
