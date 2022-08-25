from __future__ import annotations

import asyncio
import aiohttp

class ApplicationManager:
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

    async def __restart(self, /, *, app_id: int) -> dict:
        async with aiohttp.ClientSession() as ses:
            await ses.request(
                method="PUT", 
                url=f"https://api.discloud.app/v2/app/{app_id}/restart", 
                headers={"api-token": self.api_token}
            )

    async def __stop(self, /, *, app_id: int) -> dict:
        async with aiohttp.ClientSession() as ses:
            await ses.request(
                method="PUT", 
                url=f"https://api.discloud.app/v2/app/{app_id}/stop", 
                headers={"api-token": self.api_token}
            )

    def restart(self) -> None:
        self.__loop.run_until_complete(self.__restart(app_id=self.app_id))

    def stop(self) -> None:
        self.__loop.run_until_complete(self.__stop(app_id=self.app_id))
