import asyncio
import logging

import sentry_sdk
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

import bot_loader
from app import config
from app.handlers import help, join_requests
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
    await setup_commands()

    dp.include_router(help.router)
    dp.include_router(join_requests.router)

    try:
        # await dp.skip_updates()
        await dp.start_polling(bot_loader.bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot_loader.bot.session.close()


async def setup_commands():
    await bot_loader.bot.set_my_commands(DEFAULT_USER_COMMANDS,
                                         scope=BotCommandScopeAllPrivateChats())


if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            logger.info("Bot stopped!")
            exit(0)
