from sqlalchemy import Column, Integer, Boolean
from app.db.base import Base


class ChatEntry(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True)
    show_intro = Column(Boolean, nullable=False)
    only_active = Column(Boolean, nullable=False)
