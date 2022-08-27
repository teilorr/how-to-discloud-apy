from __future__ import annotations
from typing import Optional

from _discloud import (
    Terminal, 
    ApplicationManager
)

from discord.ext import commands

class Discloud:
    def __init__(self, /, *, discloud_token: str, bot: commands.Bot) -> None:
        if not isinstance(bot, commands.Bot):
            raise ValueError(
                f"Expected commands.Bot or subclass as bot, not {bot.__class__!r}"
            ) from None

        self._bot = bot
        self._terminal = Terminal(
            discloud_token=discloud_token,
            app_id=bot.user.id
        )
        self._actions = ApplicationManager(
            discloud_token=discloud_token,
            app_id=self._bot.user.id
        )

    async def restart(self, bot_id: Optional[int]=None) -> None:
        await self._actions.restart(bot_id=bot_id)
    
    async def raw_backup(self, to: Optional[int]=None) -> dict:
        return await self._actions.generate_backup(to=to)

    async def raw_app_status(self, to: Optional[int]=None) -> dict:
        return await self._actions.get_raw_status(to=to)

    async def raw_logs(self, to: Optional[str]=None) -> dict:
        return await self._terminal.fetch_full(to=to)