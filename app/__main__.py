import asyncio
import logging

import sentry_sdk
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app import config
from app.bot_loader import bot
from app.handlers import help, join_requests, group_admin, admin_changed_in_groups, bot_in_group, stat
from app.middlewares.admin import AdminMiddleware
from app.middlewares.db import DbSessionMiddleware
from loader import dp

if config.SENTRY_DSN:
    sentry_sdk.init(config.SENTRY_DSN, traces_sample_rate=0.5)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(funcName)s - %(name)s - %(message)s",
)

DEFAULT_USER_COMMANDS = [
    BotCommand(command="help", description="Помощь"),
]


async def main():
    logger.info("Starting bot")

    engine = create_async_engine(config.DATABASE_DSN, future=True, echo=False)
    db_pool = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    await setup_commands()

    dp.include_router(admin_changed_in_groups.router)
    dp.include_router(bot_in_group.router)
    dp.include_router(help.router)
    dp.include_router(join_requests.router)
    dp.include_router(group_admin.router)
    dp.include_router(stat.router)
    #
    dp.message.middleware(DbSessionMiddleware(db_pool))
    dp.message.middleware(AdminMiddleware())
    dp.my_chat_member.middleware(DbSessionMiddleware(db_pool))
    dp.chat_member.middleware(DbSessionMiddleware(db_pool))
    dp.chat_join_request.middleware(DbSessionMiddleware(db_pool))

    try:
        # await dp.skip_updates()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()


async def setup_commands():
    await bot.set_my_commands(DEFAULT_USER_COMMANDS,
                              scope=BotCommandScopeAllPrivateChats())


if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            logger.info("Bot stopped!")
            exit(0)
