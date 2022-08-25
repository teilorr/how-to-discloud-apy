from __future__ import annotations

from _discloud import DiscloudBot
from discord.ext import commands
from discord import app_commands
from utils import DotEnv
import discord

class DiscloudExamples(commands.Bot, DiscloudBot):
    def __init__(self) -> None:
        commands.Bot.__init__(
            self,
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.default()
        )

        DiscloudBot.__init__(
            self,
            discloud_token=DotEnv.get("DISCLOUD_TOKEN"),
            bot_id=DotEnv.get("BOT_ID")
        )

    async def on_ready(self) -> None:
        print(f"Entramos como {self.user}")

bot = DiscloudExamples()


bot.run(DotEnv.get("TOKEN"), log_level=40)