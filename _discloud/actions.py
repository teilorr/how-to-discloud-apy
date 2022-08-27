from __future__ import annotations
from typing import Optional

from utils.route import Route
import aiohttp

class ApplicationManager:
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

    async def generate_backup(self, to: Optional[int]=None) -> dict:
        return await self.__request(Route("GET", "/app/{app_id}/backup", app_id=to or self.app_id))

    async def get_raw_status(self, to: Optional[int]=None) -> dict:
        return await self.__request(Route("GET", "/app/{app_id}/status", app_id=to or self.app_id))

    async def restart(self, bot_id: Optional[int]=None) -> None:
        return await self.__request(Route("PUT", "/app/{app_id}/restart", app_id=bot_id or self.app_id))

    async def stop(self, bot_id: Optional[int]=None) -> None:
        return await self.__request(Route("PUT", "/app/{app_id}/stop", app_id=bot_id or self.app_id))
