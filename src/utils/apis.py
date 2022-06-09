import random

import aiohttp


async def random_beach_photo() -> str:
    """
    Get random beach picture.
    :return: hot link to the picture
    """
    resolutions = [
        "1920x1080",
        "1280x720",
        "1600x900",
        "2560x1440",
        "3840x2160",
    ]
    async with aiohttp.ClientSession(auto_decompress=False) as session:
        async with session.get(
            f"https://source.unsplash.com/{random.choice(resolutions)}/?beach"
        ) as resp:
            # unsplash returns a link to the image
            return await resp.read()
