# -*- coding: utf-8 -*-
import warnings

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from pytz_deprecation_shim import PytzUsageWarning

from src import config
from src.utils import get_version

warnings.filterwarnings(action="ignore", category=PytzUsageWarning)
storage = RedisStorage.from_url(config.REDIS_URL, connection_kwargs={"max_connections": 256},
                                data_ttl=1000000, state_ttl=1000000)
dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.CHAT)

app_version = get_version()
