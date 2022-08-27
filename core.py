from __future__ import annotations

from _discloud import Discloud
from discord.ext import commands
from utils import DotEnv
import pathlib
import discord

class DiscloudBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.default()
        )

    async def setup_hook(self) -> None:
        self.discloud = Discloud(
            discloud_token=DotEnv.get("DISCLOUD_TOKEN"),
            bot=self
        )
        # Carrega todos os arquivos em "./cogs" que terminam em ".py", exceto os que começam com "_"
        for file in pathlib.Path("./cogs").glob("**/[!_]*.py"):
            extension = ".".join(file.parts) \
                            .removesuffix(".py")

            await self.load_extension(extension)

    async def on_ready(self) -> None:
        print(f"Entramos como {self.user}")

bot = DiscloudBot()
bot.run(DotEnv.get("TOKEN"), log_level=40)