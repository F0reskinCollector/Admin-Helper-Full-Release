import discord
import aiofiles
import aiofiles.os
from discord.ext import commands


#   def check_if_user_has_premium(ctx):
#    with aiofiles.open("premium_user.txt") as f:
#        premium_users_list = await f.read(f)
#        if ctx.author.mention not in premium_users_list:
#            return False
##
#    return True


class premium(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def whitelist(self, ctx, member: discord.Member):
        try:
            async with aiofiles.open(f'premium_user.txt', mode="a") as file:
                await file.write(f"{member.id}\n")
            async with aiofiles.open(f'premium.txt', mode="a") as file:
                await file.write(f"{member.mention}\n")
            embed = discord.Embed(title=f"", description=f"I whitelisted {member.mention}!")
            await ctx.send(embed=embed)
        except PermissionError:
            embed = discord.Embed(title=f"", description=f"You dont have permissions to perform this command.")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def delpremium(self, ctx):
        embed = discord.Embed(title=f"", description=f"To remove a user please go to ``premium_user`` and ``premium`` and delete the ID of the User.")
        await ctx.send(embed=embed)

    @commands.command()
    async def whitelisted(self, ctx):
        async with aiofiles.open(f"premium.txt", mode="r") as f:
            contents = await f.read()
            embed = discord.Embed(title="All whitelisted user;", description=f"{contents}")
            await ctx.send(embed=embed)


    #ids = ["834530511790538763", "486930148701241354"]

    @commands.command()
    async def sudo(self, ctx, member: discord.Member, *, message=None):
        with open('premium_user.txt', 'r') as file:
            ids = tuple((int(x.strip()) for x in file.readlines() if x.strip().isdecimal()))
            if ctx.message.author.id in ids:
        #   async with aiofiles.open(f"premium_user.txt", mode="r") as f:
        #       content = await f.readlines()
        #       if ctx.author.name in content:
                await ctx.message.delete()
                webhooks = await ctx.channel.webhooks()
                webhook = await ctx.channel.create_webhook(name=member.name)
                await webhook.send(str(message),
                                   username=member.name,
                                   avatar_url=member.avatar_url)
                for webhook in webhooks:
                    await webhook.delete()
            else:
                embed = discord.Embed(title="", description="**Hey! You arent authorized to use this command.**",
                                      colour=0x992d22)
                embed.add_field(name="How to get access?", value="Message the Creator of the bot or use the -bugreport command and ask for permissions.")
                embed.add_field(name="Why do you need permissions?", value="You need permissions to use this command so it doesnt come in the wrong hands.")
                await ctx.send(embed=embed)

    @whitelist.error
    async def addpremium_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**",
                                  colour=0x992d22)
            await ctx.send(embed=embed)

    #@commands.command()
    #async def bot(self, ctx):
    #    await ctx.send("test")
    #    embed = discord.Embed(title="About me!", description="", colour=0x7289da)
    #    embed.add_field(name="Languages I support", value=f"Currently I only support English <:Ameritan:808821635741908992>")
    #    embed.add_field(name="Programming language", value=f"Python (1.7.3) <:python:286529073445076992>")
    #    embed.add_field(name=f"What am I?", value=f"I'm a multipurpose bot, you can use me for `Moderation`, `Fun` or something else.")
    #    embed.add_field(name=f"Where was I created?", value=f"I was made in Germany near Munich.")
    #    embed.add_field(name=f"When was I created?", value=f"{self.bot.application_info()}")
    #    embed.add_field(name=f"Ping", value=f"{self.bot.latency}")
    #    await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(premium(bot))
