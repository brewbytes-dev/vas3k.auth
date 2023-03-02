from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.config import DEVELOPER_ID


class DeveloperFilter(BaseFilter):
    is_developer: bool

    def __init__(self, is_developer: bool):
        self.is_developer = is_developer

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return (str(DEVELOPER_ID) == str(message.chat.id)) == self.is_developer
