from aiogram.types import Message

from app.backend.chat import ChatBackend
from app.db.models import ReleaseNotes


async def get_latest_notes(message: Message, chat_backend: ChatBackend) -> str | None:
    chat_id = message.chat.id
    await chat_backend.get_or_create(chat_id)
    notes: list[ReleaseNotes] = await chat_backend.get_unaware_release_notes(chat_id)
    notes_text = build_notes_message(notes)
    return notes_text


def build_notes_message(notes: list[ReleaseNotes]) -> str | None:
    if not notes:
        return None

    notes_text = "📬 Обновления в боте:\n\n"
    for note in notes:
        notes_text += (f"🔹 {note.version}:\n"
                       f"{note.notes}\n\n")

    return notes_text
