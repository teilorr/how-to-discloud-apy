from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

from discord.ext import commands

if TYPE_CHECKING:
    from core import DiscloudBot

class GeneralCommands(commands.Cog, name="Comandos gerais"):
    def __init__(self, bot: DiscloudBot) -> None:
        self.bot = bot

    @commands.command(name="sync")
    async def _sync_slash(self, ctx: commands.Context) -> None:
        synced = await self.bot.tree.sync()
        await ctx.send(f"Sincronizei {len(synced)} comandos para o discord!")

    @commands.command(name="ping")
    async def _ping(self, ctx: commands.Context) -> None:
        await ctx.send(f"> `{self.bot.latency:.4f}ms`")

async def setup(bot: DiscloudBot) -> None:
    await bot.add_cog(GeneralCommands(bot))