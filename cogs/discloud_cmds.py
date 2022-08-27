from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Optional
)

from dateutil import parser as dateutil_parser
from discord.ext import commands
from discord import app_commands
from utils import is_number
import discord

if TYPE_CHECKING:
    from core import DiscloudBot

class DiscloudCommands(commands.Cog, name="Comandos da Discloud"):
    def __init__(self, bot: DiscloudBot) -> None:
        self.bot = bot

    @app_commands.command(name="terminal", description="Mostra o terminal da aplicação")
    async def show_terminal(self, interaction: discord.Interaction, app_id: Optional[str]=None) -> None:
        if not is_number(app_id):
            return
        app_id = int(app_id.strip())

        logs = await self.bot.discloud.raw_logs(to=app_id)
        if logs["status"] == "error":
            embed = discord.Embed(
                title="Erro!",
                description=f"Tivemos um erro ao consultar o terminal da sua aplicação: ```{logs['message']}```",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=embed)

        embed = discord.Embed(
            title="Terminal",
            description=f"```{logs['apps']['terminal']['small']}```",
            color=discord.Color.brand_green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="backup", description="Gera um link pro backup da sua aplicação")
    async def show_backup(self, interaction: discord.Interaction, app_id: Optional[str]=None) -> None:
        if not is_number(app_id):
            return
        app_id = int(app_id.strip())

        await interaction.response.defer()
 
        bkcup_raw = await self.bot.discloud.raw_backup(to=app_id)
        if bkcup_raw["status"] == "error":
            embed = discord.Embed(
                title="Erro!",
                description=f"Tivemos um erro ao gerar o backup da sua aplicação: ```{bkcup_raw['message']}```",
                color=discord.Color.red()
            )
            return await interaction.followup.send(embed=embed)

        embed = discord.Embed(
            title="Backup",
            description=f"O Backup da sua aplicação está pronto! Basta [apertar aqui]({bkcup_raw['backups']['url']}) para baixar os arquivos",
            color=discord.Color.brand_green()
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="status", description="Mostra informações sobre seu bot na discloud")
    async def show_status(self, interaction: discord.Interaction, app_id: Optional[str]=None) -> None:
        if not is_number(app_id):
            return
        app_id = int(app_id.strip())

        raw_status = await self.bot.discloud.raw_app_status(to=app_id)
        if raw_status["status"] == "error":
            embed = discord.Embed(
                title="Erro!",
                description=f"Tivemos um erro ao buscar informações da sua aplicação: ```{raw_status['message']}```",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=embed)

        apps = raw_status["apps"]
        on_discloud = await self.bot.fetch_user(app_id or apps["id"])

        embed = discord.Embed(
            title=f"Status de {on_discloud.name} na discloud",
            color=discord.Color.brand_green()
        )
        embed.add_field(name="\U0001f530 `Nome`", value=f"***{on_discloud}***")
        embed.add_field(name="\U0001f6a2 `Container`", value=f"***{apps['container']}***")
        embed.add_field(name="\U0001f5a5 `CPU`", value=f"***{apps['cpu']}***", inline=False)
        embed.add_field(name="\U0001f4be `RAM`", value=f"***{apps['memory']}***")
        embed.add_field(name="\U0001f503 `Último restart`", value=f"***{discord.utils.format_dt(dateutil_parser.parse(apps['startedAt']), 'R')}***", inline=False)
        embed.set_thumbnail(url=on_discloud.avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot: DiscloudBot) -> None:
    await bot.add_cog(DiscloudCommands(bot))