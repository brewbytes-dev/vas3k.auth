from aiogram import Bot

from src import config


class AuthBot(Bot):
    ...


bot = AuthBot(config.BOT_TOKEN)
