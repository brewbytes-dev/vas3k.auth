import logging

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatEntry

logger = logging.getLogger(__name__)


class RepoChat:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_or_create(self, chat_id: int) -> ChatEntry:
        async with self.session.begin():
            stmt = select(ChatEntry).filter_by(chat_id=chat_id)
            try:
                result = await self.session.execute(stmt)
                instance = result.scalars().first()
                if instance:
                    return instance
            except NoResultFound:
                pass

            instance = ChatEntry(chat_id=chat_id)
            self.session.add(instance)
            await self.session.commit()

            return instance

    async def update_chat_id(self, old_chat_id: int, new_chat_id: int) -> bool:
        async with self.session.begin():
            stmt = select(ChatEntry).filter_by(chat_id=old_chat_id)
            result = await self.session.execute(stmt)
            instance = result.scalars().first()
            if instance:
                instance.chat_id = new_chat_id
                await self.session.commit()
                return True
            return False

    async def get_all(self) -> list[ChatEntry]:
        async with self.session.begin():
            stmt = select(ChatEntry)
            result = await self.session.execute(stmt)
            return list(result.scalars().all())

    async def switch_show_intro(self, chat_id: int) -> bool:
        async with self.session.begin():
            stmt = select(ChatEntry).filter_by(chat_id=chat_id)
            result = await self.session.execute(stmt)
            instance = result.scalars().first()
            instance.show_intro = not instance.show_intro
            await self.session.commit()
            return instance.show_intro

    async def switch_only_active(self, chat_id: int) -> bool:
        async with self.session.begin():
            stmt = select(ChatEntry).filter_by(chat_id=chat_id)
            result = await self.session.execute(stmt)
            instance = result.scalars().first()
            instance.only_active = not instance.only_active
            await self.session.commit()
            return instance.only_active
