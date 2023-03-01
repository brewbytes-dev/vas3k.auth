import re
from pathlib import Path

from aiogram import Bot

from app import config

__all__ = ['bot']


def _get_version():
    here = Path(__file__).absolute().parent
    entry = (here / '__version__.py').read_text('utf-8')

    try:
        version = re.findall(r"^__version__ = \"([^']+)\"\r?$", entry, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

    return version


class AuthBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._version = None

    @property
    def version(self):
        if self._version is None:
            self._version = _get_version()
        return self._version


bot = AuthBot(config.BOT_TOKEN)
