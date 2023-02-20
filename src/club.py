import logging
import aiohttp

from config import JWT_TOKEN


logger = logging.getLogger(__name__)
VAS3K_ENDPOINT = "https://vas3k.club"
USER = "/user"


def parse_membership(user_slug):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{VAS3K_ENDPOINT}{USER}/{user_slug}.json",
                params={"jwt": JWT_TOKEN}
            ) as response:
                return await response.json()
    except Exception as e:
        logger.exception(e)
        return None
