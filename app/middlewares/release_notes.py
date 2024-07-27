from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject

from app.backend.chat import ChatBackend
from app.repos.chat_requests import RepoRequests
from app.repos.chats import RepoChat
from app.repos.release_notes import RepoReleaseNotes


class ReleaseNotesMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        rn = get_flag(data, "release_notes")
        if not rn:
            return await handler(event, data)
