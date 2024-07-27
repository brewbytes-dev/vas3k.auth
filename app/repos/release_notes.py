import logging

from packaging import version
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatEntry, ReleaseNotes, ChatVersionAware

logger = logging.getLogger(__name__)


class RepoReleaseNotes:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_all(self) -> list[ReleaseNotes]:
        async with self.session.begin():
            stmt = select(ReleaseNotes)
            result = await self.session.execute(stmt)
            return list(result.scalars().all())

    async def get_unaware_release_notes(self, chat_id: int, latest_ver: str) -> list[ReleaseNotes]:
        async with self.session.begin():
            # Query the latest version the chat is aware of
            subquery = select(ChatVersionAware.version). \
                where(ChatVersionAware.chat_id == chat_id). \
                order_by(ChatVersionAware.version.desc()). \
                limit(1)

            latest_known_version = await self.session.execute(subquery)
            latest_known_version = latest_known_version.scalars().first()

            # If the chat is not aware of any versions, set a low comparison base
            if not latest_known_version:
                latest_known_version = latest_ver

            # Query all release notes with a higher version than the latest known
            release_notes_query = select(ReleaseNotes). \
                where(ReleaseNotes.version > latest_known_version). \
                order_by(ReleaseNotes.version)

            release_notes = await self.session.execute(release_notes_query)
            release_notes_list = [note for note in release_notes.scalars().all()]

            return release_notes_list

    async def set_chat_awared_version(self, chat_id: int, ver: str):
        async with self.session.begin():
            instance = ChatVersionAware(chat_id=chat_id, version=ver)
            await self.session.merge(instance)
            await self.session.commit()
