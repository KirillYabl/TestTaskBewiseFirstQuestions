import typing

import aiohttp


async def get_random_questions(aiohttp_session: aiohttp.ClientSession, count: int) -> list[dict[str, typing.Any]]:
    params = {
        "count": count
    }
    async with aiohttp_session.get("https://jservice.io/api/random", params=params) as response:
        response.raise_for_status()
        return await response.json()
