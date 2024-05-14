from typing import Annotated, Optional

from sqlalchemy import Column, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.base import Base, bigint

int_primary = Annotated[bigint, mapped_column(primary_key=True)]
str_primary = Annotated[str, mapped_column(primary_key=True)]
int_primary_incr = Annotated[bigint, mapped_column(primary_key=True, autoincrement=True)]


class ChatEntry(Base):
    __tablename__ = "chats"

    id: Mapped[int_primary_incr]
    chat_id: Mapped[bigint] = mapped_column(nullable=False, index=True)
    show_intro: Mapped[bool] = mapped_column(default=True)
    only_active: Mapped[bool] = mapped_column(default=False)
    follow_up_requests: Mapped[bool] = mapped_column(default=False)
    request_texts = relationship("RequestText", back_populates="chat", cascade="all, delete, delete-orphan")
    unregistered_requests = relationship("UnregisteredRequests", back_populates="chat", cascade="all, delete, delete-orphan")
    chat_version_aware = relationship("ChatVersionAware", back_populates="chat", cascade="all, delete, delete-orphan")


class RequestText(Base):
    __tablename__ = "request_texts"

    id: Mapped[int_primary_incr]
    chat_id: Mapped[bigint] = Column(BigInteger, ForeignKey('chats.chat_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False )
    text: Mapped[str] = mapped_column(nullable=False,
                                      default="✋ Привет! Наш чат только для людей из Вастрик.Клуба!\n"
                                              "Расскажи о себе и своей связи с клубом и почему хочешь в чат. "
                                              "Мы ответим!")
    chat = relationship("ChatEntry", back_populates="request_texts")


class UnregisteredRequests(Base):
    __allow_unmapped__ = True
    __tablename__ = "user_requests"

    req_id: Mapped[int_primary_incr]
    chat_id: Mapped[bigint] = Column(BigInteger, ForeignKey('chats.chat_id', onupdate="CASCADE", ondelete="CASCADE"),
                                     nullable=False)
    user_id: Mapped[bigint]
    message_id: Optional[Mapped[bigint]] = Column(BigInteger, nullable=True)
    sent: Optional[Mapped[bool]] = Column(Boolean, default=False)
    sent_message_id: Optional[Mapped[bigint]] = Column(BigInteger, nullable=True)
    chat = relationship("ChatEntry", back_populates="unregistered_requests")


class ReleaseNotes(Base):
    __tablename__ = "release_notes"

    id: Mapped[int_primary_incr]
    version: Mapped[str]
    notes: Mapped[str]


class ChatVersionAware(Base):
    __tablename__ = "chat_version_aware"

    id: Mapped[int_primary_incr]
    chat_id: Mapped[bigint] = Column(BigInteger, ForeignKey('chats.chat_id', onupdate="CASCADE", ondelete="CASCADE"),
                                     nullable=False)

    version: Mapped[str] = mapped_column(nullable=False)
    chat = relationship("ChatEntry", back_populates="chat_version_aware")
