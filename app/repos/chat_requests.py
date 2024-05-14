import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UnregisteredRequests

logger = logging.getLogger(__name__)


class RepoRequests:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, chat_id: int, user_id: int) -> UnregisteredRequests:
        async with self.session.begin():
            stmt = select(UnregisteredRequests).filter_by(chat_id=chat_id, user_id=user_id)
            result = await self.session.execute(stmt)
            return result.scalars().first()

    async def create(self, chat_id: int, user_id: int, message_id: int) -> UnregisteredRequests:
        async with self.session.begin():
            req = UnregisteredRequests(chat_id=chat_id, user_id=user_id, message_id=message_id)
            self.session.add(req)
            await self.session.commit()
            return req

    async def get_by_message_id(self, user_id: int, message_id: int) -> UnregisteredRequests | None:
        async with self.session.begin():
            stmt = select(UnregisteredRequests).filter_by(user_id=user_id, message_id=message_id)
            result = await self.session.execute(stmt)
            return result.scalars().first()

    async def mark_as_sent(self, req_id: int, message_id: int):
        async with self.session.begin():
            stmt = update(UnregisteredRequests).filter_by(req_id=req_id).values(sent_message_id=message_id, sent=True)
            await self.session.execute(stmt)
            await self.session.commit()
