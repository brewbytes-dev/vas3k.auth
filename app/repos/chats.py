import logging

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatEntry, RequestText

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

    async def get_follow_up_requests_status(self, chat_id: int) -> bool:
        async with self.session.begin():
            stmt = select(ChatEntry).filter_by(chat_id=chat_id)
            result = await self.session.execute(stmt)
            instance = result.scalars().first()
            return instance.follow_up_requests

    async def turn_on_follow_up_requests(self, chat_id: int, text: str = None) -> str:
        async with self.session.begin():
            stmt = select(RequestText).filter_by(chat_id=chat_id)
            result = await self.session.execute(stmt)
            instance = result.scalars().one_or_none()

            if instance is None:
                instance = RequestText(chat_id=chat_id)

            if text is not None:
                instance.text = text

            await self.session.merge(instance)
            await self.session.refresh(instance)

            stmt = update(ChatEntry).where(ChatEntry.chat_id == chat_id).values(
                follow_up_requests=True,
            )
            await self.session.execute(stmt)
            await self.session.commit()

            return instance.text

    async def turn_off_follow_up_requests(self, chat_id: int):
        async with self.session.begin():
            stmt = update(ChatEntry).where(ChatEntry.chat_id == chat_id).values(follow_up_requests=False)
            await self.session.execute(stmt)
            await self.session.commit()

    async def get_follow_up_request_text(self, chat_id: int) -> None | str:
        async with self.session.begin():
            stmt = select(RequestText).filter_by(chat_id=chat_id)
            result = await self.session.execute(stmt)
            instance = result.scalars().one_or_none()

            if instance is None:
                return None

            return instance.text
