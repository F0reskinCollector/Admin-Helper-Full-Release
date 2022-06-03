import discord
import discord.components
from discord import ui, app_commands
from discord.ext import commands
from datetime import datetime
import asyncio

class modal(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id=887806058347790406))
            self.synced = True
        print("modal loaded")


class my_modal(ui.Modal, title = "Bugreport"):
    answer = ui.TextInput(label= "Test", style= discord.TextStyle.short, placeholder= "Yes?", default = "Yes/No", required= False, max_length= 20)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title = self.title, description=f"**{self.answer.label}**\n{self.answer}", timestamp = datetime.now(), color=discord.Color.blue())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed, ephemeral = True)

def setup(bot: commands.Bot):
    bot.add_cog(modal(bot))
