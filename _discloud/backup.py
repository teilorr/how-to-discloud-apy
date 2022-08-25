from __future__ import annotations

import asyncio
import aiohttp

class Backup:
    def __init__(self, /, *, discloud_token: str, app_id: int) -> None:
        if not isinstance(app_id, int):
            raise ValueError(
                f"Expected int as app_id, not {app_id.__class__!r}"
            ) from None

        self.app_id = app_id
        self.api_token = discloud_token
        self.__loop = asyncio.get_event_loop()

    def __del__(self) -> None:
        if not self.__loop.is_closed():
            self.__loop.close()

    async def __generate(self, /, *, app_id: int) -> dict:
        async with aiohttp.ClientSession() as ses:
            async with ses.request("GET", f"https://api.discloud.app/v2/app/{app_id}/backup", headers={"api-token": self.api_token}) as response:
                return await response.json()

    @property
    def download_url(self):
        return self.__loop.run_until_complete(self.__generate(app_id=self.app_id))["backups"]["url"]
