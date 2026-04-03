from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.exc import DBAPIError

from app.repos.chats import RepoChat


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
        try:
            async with self.session_pool() as session:
                data["repo_chat"] = RepoChat(session)
                return await handler(event, data)
        except DBAPIError as exc:
            # Transient asyncpg disconnects happen on stale pooled connections; retry once.
            exc_text = str(exc).lower()
            transient_db_markers = (
                "connection was closed in the middle of operation",
                "remaining connection slots are reserved for non-replication superuser connections",
                "consuming input failed",
            )
            if not any(marker in exc_text for marker in transient_db_markers):
                raise
            async with self.session_pool() as session:
                data["repo_chat"] = RepoChat(session)
                return await handler(event, data)
