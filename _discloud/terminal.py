from __future__ import annotations
from typing import (
    Optional
)

from utils.route import Route
import aiohttp

class Terminal:
    def __init__(self, /, *, discloud_token: str, app_id: int) -> None:
        if not isinstance(app_id, int):
            raise ValueError(
                f"Expected int as app_id, not {app_id.__class__!r}"
            ) from None

        self.app_id = app_id
        self.api_token = discloud_token

    async def __request(self, route: Route) -> dict:
        async with aiohttp.ClientSession() as ses: 
            async with ses.request(
                        method=route.method, 
                        url=route.url, 
                        headers={"api-token": self.api_token}
                    ) as response:
                return await response.json()

    async def fetch_full(self, to: Optional[int]=None) -> dict:
        return await self.__request(Route("GET", "/app/{app_id}/logs", app_id=to or self.app_id))