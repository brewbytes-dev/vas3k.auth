import logging
import aiohttp

from config import JWT_TOKEN

logger = logging.getLogger(__name__)
VAS3K_ENDPOINT = "https://vas3k.club"
BY_TELEGRAM_ID = "/by_telegram_id"
USER = "/user"


async def get_member_by_username(username):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{VAS3K_ENDPOINT}{USER}/{username}.json?service_token={JWT_TOKEN}",
                params={"service_token": JWT_TOKEN}
            ) as response:
                return await response.json()
    except Exception as e:
        logger.exception(e)
        return None


async def get_member_by_telegram_id(telegram_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{VAS3K_ENDPOINT}{USER}{BY_TELEGRAM_ID}/{telegram_id}.json",
                params={"service_token": JWT_TOKEN}
            ) as response:
                return await response.json()
    except Exception as e:
        logger.exception(e)
        return None
