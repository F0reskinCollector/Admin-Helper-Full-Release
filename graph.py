import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import asyncio
import discord
from discord.ext import commands
import os
import time
import io

class diagram(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def create_score_bargraph(ctx, percentage_list, votes_list):
    x_labels = ['1','2','3','4','5','6','7','8','9','10']

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(x_labels, votes_list)
    plt.show()

    filename = "test.png"
    plt.savefig(filename)
    image = discord.File(filename)

    await ctx.send(file = image)

    plt.close()


def setup(bot: commands.Bot):
    bot.add_cog(diagram(bot))
