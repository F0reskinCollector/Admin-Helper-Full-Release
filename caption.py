import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands


class caption(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def caption(self, ctx, *, text):

        img = Image.open(f"{ctx.message.attachments}")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 24)

        draw.text((0, 150), text, (0, 0, 0), font=font)
        img.save("1.png")
        await ctx.send(file=discord.File("1.png"))

    @commands.command()
    async def cogtest(self, ctx):
        await ctx.send("Does work")


def setup(bot: commands.Bot):
    bot.add_cog(caption(bot))
