from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.backend.chat import ChatBackend
from app.repos.chat_requests import RepoRequests
from app.repos.chats import RepoChat
from app.repos.release_notes import RepoReleaseNotes


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["chat_backend"] = ChatBackend(
                RepoChat(session),
                RepoRequests(session),
                RepoReleaseNotes(session)
            )

            data["repo_chat"] = RepoChat(session)
            data["repo_requests"] = RepoRequests(session)
            return await handler(event, data)
