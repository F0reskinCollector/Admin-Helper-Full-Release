import discord
import aiofiles
from datetime import datetime
import aiofiles.os
from discord.ext import commands

class antialts(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def member_on_join(self, message, member: discord.Member):
        created = member.created_at
        now = datetime.now()
        delta = (now - created).days

        if delta < 10:
            await member.send(f'Hello there {member.mention}! I saw that your account is {delta} days old! Please wait till your account is 10 Days old!')
            await member.kick()
            await message.channel.send('Detected alt account and kicked it!')


def setup(bot: commands.Bot):
    bot.add_cog(antialts(bot))
