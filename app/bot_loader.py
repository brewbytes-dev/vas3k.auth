from aiogram import Bot

from app import config


class AuthBot(Bot):
    ...


bot = AuthBot(config.BOT_TOKEN)
