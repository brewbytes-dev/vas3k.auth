from app.db.models import ReleaseNotes
from app.repos.chat_requests import RepoRequests
from app.repos.chats import RepoChat
from app.repos.release_notes import RepoReleaseNotes

from app.bot_loader import _get_version


class ChatBackend:
    def __init__(self, repo_chats: RepoChat,
                 repo_chat_requests: RepoRequests,
                 repo_release_notes: RepoReleaseNotes):
        self.repo_chats = repo_chats
        self.repo_chat_requests = repo_chat_requests
        self.repo_release_notes = repo_release_notes

    async def get_all_chats(self):
        return await self.repo_chats.get_all()

    async def get_or_create(self, chat_id: int):
        chat_entry = await self.repo_chats.get(chat_id)

        if chat_entry is not None:
            return chat_entry

        chat_entry = await self.repo_chats.create(chat_id)

        code_version = _get_version()
        await self.repo_release_notes.set_chat_awared_version(chat_id, code_version)

        return chat_entry

    async def get_follow_up_request_text(self, chat_id: int) -> str:
        return await self.repo_chats.get_follow_up_request_text(chat_id)

    async def update_chat_id(self, old_chat_id: int, new_chat_id: int) -> bool:
        return await self.repo_chats.update_chat_id(old_chat_id, new_chat_id)

    async def get_user_request(self, chat_id: int, user_id: int):
        return await self.repo_chat_requests.get(chat_id, user_id)

    async def create_user_request(self, chat_id: int, user_id: int, message_id: int):
        return await self.repo_chat_requests.create(chat_id, user_id, message_id)

    async def get_request_by_message_id(self, chat_id: int, message_id: int):
        return await self.repo_chat_requests.get_by_message_id(chat_id, message_id)

    async def mark_request_as_sent(self, req_id: int, message_id: int):
        return await self.repo_chat_requests.mark_as_sent(req_id, message_id)

    async def switch_show_intro(self, chat_id: int) -> bool:
        return await self.repo_chats.switch_show_intro(chat_id)

    async def switch_only_active(self, chat_id: int) -> bool:
        return await self.repo_chats.switch_only_active(chat_id)

    async def get_follow_up_requests_status(self, chat_id: int) -> bool:
        return await self.repo_chats.get_follow_up_requests_status(chat_id)

    async def turn_on_follow_up_requests(self, chat_id: int, text: str = None) -> str:
        return await self.repo_chats.turn_on_follow_up_requests(chat_id, text)

    async def turn_off_follow_up_requests(self, chat_id: int) -> bool:
        return await self.repo_chats.turn_off_follow_up_requests(chat_id)

    async def get_unaware_release_notes(self, chat_id: int) -> list[ReleaseNotes]:
        notes = await self.repo_release_notes.get_unaware_release_notes(chat_id, _get_version())
        return notes

    async def set_chat_awared_version(self, chat_id: int):
        return await self.repo_release_notes.set_chat_awared_version(chat_id, _get_version())

    async def get_release_notes(self) -> list[ReleaseNotes]:
        return await self.repo_release_notes.get_all()
