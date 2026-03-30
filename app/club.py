import logging
import json
from dataclasses import dataclass, fields

import aiohttp

from config import JWT_TOKEN

logger = logging.getLogger(__name__)
VAS3K_ENDPOINT = "https://vas3k.club"
BY_TELEGRAM_ID = "/by_telegram_id"
USER = "/user"


async def _parse_json_response(response: aiohttp.ClientResponse) -> dict | None:
    if response.status != 200:
        logger.warning("Club API request failed: status=%s url=%s", response.status, response.url)
        return None

    response_body = await response.text()
    try:
        parsed = json.loads(response_body)
    except json.JSONDecodeError:
        logger.warning(
            "Club API returned non-JSON response: content_type=%s url=%s",
            response.headers.get("Content-Type"),
            response.url,
        )
        return None

    if not isinstance(parsed, dict):
        logger.warning("Club API returned unexpected payload type: %s", type(parsed).__name__)
        return None
    return parsed


@dataclass(init=False)
class ClubUser:
    full_name: str
    slug: str
    moderation_status: str
    is_active_member: bool

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)

    @property
    def user_link(self):
        return f"{VAS3K_ENDPOINT}{USER}/{self.slug}"

    @property
    def approved(self):
        return self.moderation_status == "approved"


async def get_member_by_username(username):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{VAS3K_ENDPOINT}{USER}/{username}.json?service_token={JWT_TOKEN}",
                params={"service_token": JWT_TOKEN}
            ) as response:
                return await _parse_json_response(response)
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
                return await _parse_json_response(response)
    except Exception as e:
        logger.exception(e)
        return


async def user_by_telegram_id(telegram_id) -> ClubUser | None:
    club_profile = await get_member_by_telegram_id(telegram_id)
    if not club_profile:
        return None

    user_profile: dict = club_profile.get('user')

    if not user_profile:
        return None

    return ClubUser(**user_profile)
