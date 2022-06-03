import asyncio
import io
import json

import aiofiles
from discord.ext import tasks, forms
import random
import time
from datetime import datetime
import discord
import discord.ext
from pythonping import ping
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands.context import Context
#from discord_components import DiscordComponents, Button
from discord_slash import SlashCommand, SlashContext


intents = discord.Intents.default()
intents.members = True


def get_prefix(bot_obj, message: Context) -> str:
    try:
        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]

    except AttributeError:
        return '-'

    except KeyError:
        return '-'


bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command('help')
#bot.remove_command('diagram')
bot.load_extension('premium')
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

error = [f"Something went wrong here. Please try again in a few minutes.\nIf this still continues please use -bugreport!"]

#async def status_task():
#    while True:
#        await bot.change_presence(
#           activity=discord.Activity(type=discord.ActivityType.listening, name='your commands! / -help'),
#           status=discord.Status.dnd)
#        await asyncio.sleep(20)
#        await bot.change_presence(
#           activity=discord.Activity(type=discord.ActivityType.listening, name='Expected Downtime! / -help'),
#           status=discord.Status.dnd)
#        await asyncio.sleep(10)

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name='your commands! / -help'),
        status=discord.Status.dnd)
    #DiscordComponents(bot)
    print('Eingeloggt daddy')


@bot.listen()
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(color=discord.Color(value=0x36393e))
            embed.set_author(name="Here's some stuff to get you started:")
            embed.add_field(name="Prefix", value="`-`", inline=False)
            embed.add_field(name="Command help", value="You can use `-help`!", inline=False)
            embed.add_field(name="Support Server",
                            value="[Admin Helper Support](https://discord.gg/wY3Q4PJHJk)", inline=False)
            embed.add_field(name="Upvote", value="[Click here](https://discordbotlist.com/bots/admin-helper/upvote)")
            embed.set_footer(text=f"Thanks to you, Admin Helper is now on {len(bot.guilds)} servers!",
                             icon_url=f"{bot.user.avatar_url}")
            #embed = discord.Embed(title="Thanks for inviting me!",description="**__Introduction__**\nHello i'm ALL, a powerful bot that can moderate your server, or make him active with fun commands!\n**__Useful commands__**\nStart by typing `a!help` to see all the commands!\nUse `a!setprefix` - to set a custom prefix for your server!",color=0x0055ff)
            await channel.send(embed=embed)
        break


#@bot.command(
#    name="base_command",
#    description="This description isn't seen in UI (yet?)",
#    options=[
#        interactions.Option(
#            name="command_name",
#            description="A descriptive description",
#            type=interactions.OptionType.SUB_COMMAND,
#            options=[
#                interactions.Option(
#                    name="option",
#                    description="A descriptive description",
#                    type=interactions.OptionType.INTEGER,
#                    required=False,
#                ),
#        interactions.Option(
#            name="second_command",
#            description="A descriptive description",
#            type=interactions.OptionType.SUB_COMMAND,
#            options=[
#                interactions.Option(
#                    name="second_option",
#                    description="A descriptive description",
#                    type=interactions.OptionType.STRING,
#                    required=True,
#                ),
#            ],
#        ),
#    ],
#)
#async def cmd(ctx: interactions.CommandContext, sub_command: str, second_option: str, option: int = None):
#    if sub_command == "command_name":
#      await ctx.send(f"You selected the command_name sub command and put in {option}")
#    elif sub_command == "second_command":
#      await ctx.send(f"You selected the second_command sub command and put in {second_option}")

@bot.command()
async def language(ctx):
    embed = discord.Embed(description=f"Hello there {ctx.author.mention}!")
    embed.add_field(name="We have discontinued this command!", value="Please try sometime in the future!")
    await ctx.reply(embed=embed)


#@bot.command()
#async def buttons(ctx):
#    try:
#        await ctx.send(
#            "Hello, World!",
#            components=[
#                Button(label="button!")
#            ]
#        )
#
#        interaction = await bot.wait_for("button_click", check=lambda i: i.component.label.startswith("button!"))
#        await interaction.respond(content="Button clicked!", ephemeral=True)
#    except Exception as e:
#        print(e)


@bot.command(pass_context=True, aliases=["PREFIX", "Prefix", "pREFIX"])
@has_permissions(administrator=True)
async def prefix(ctx: Context, new_prefix: str = None):
    if ctx.guild is None:
        await ctx.reply("**You cannot change the prefix outside of a server silly!**")
        return

    if new_prefix is None:
        embed = discord.Embed(title="**Usage**", description=f"You can customize the Prefix using\n`-prefix [Your prefix]`!", colour=0x992d22)
        await ctx.send(embed=embed)
        return

    if len(new_prefix) > 5:
        await ctx.reply("**Prefix cannot be longer than 5 characters!**")
        return

    if new_prefix == '-':
        embed = discord.Embed(title="**I have set/reset the Prefix!**", description=f"`{new_prefix}`", colour=0x992d22)
        await ctx.guild.me.edit(nick=f"Admin Helper")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = new_prefix

        with open("prefixes.json", 'w') as f:
            json.dump(prefixes, f, indent=4)
    else:
        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = new_prefix

        with open("prefixes.json", 'w') as f:
            json.dump(prefixes, f, indent=4)
            embed = discord.Embed(title="**Prefix changed to:**", description=f"`{new_prefix}`", colour=0x992d22)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"Also named myself to Admin Helper ({new_prefix})")
            await ctx.guild.me.edit(nick=f"Admin Helper ({new_prefix})")
            await ctx.send(embed=embed)


class colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5

@bot.command()
async def giveaway(ctx):
    form = Form(ctx,'Giveaway')
    form.add_question('How long should the giveaway last?','first')
    form.edit_and_delete(True)
    await form.set_color("#992d22")
    result = await form.start()
    if result.first == int(0 - 10):
        await asyncio.sleep(result.first)
        await ctx.send("times up")
    #embed = discord.Embed(title="Your results!", description=f"Set the time to {result.first}")
    #await ctx.send(embed=embed)
    return result



@bot.command()
async def updates(ctx):
    embed = discord.Embed(title="**Updates**", description="", colour=0xe74c3c)
    embed.add_field(name="**5/2/22 - 8:10 PM**", value="Prefix Changed To '?' To Prevent Interferes With MEE6.",
                    inline=True)
    embed.add_field(name="**6/2/22 - 9:20 PM**",
                    value="Prefix Changed To '-' To Prevent Interferes With Dyno And Carl Bot.", inline=True)
    embed.add_field(name="**8/2/22 - 11:28 PM European Time**", value="Added Logs To Console To Prevent Uptime Issues.",
                    inline=True)
    embed.add_field(name="**9/2/22 - 11:30 PM European Time**", value="Removed Logs And Switched Hoster.", inline=True)
    embed.add_field(name="**13/2/22 - 03:00 AM European Time**", value="Added Customizable Prefix.", inline=True)
    embed.add_field(name="**14/2/22 - 04:46 To 7:45 AM European Time**",
                    value="Reworked The Gayrate And Ballsize Generator.", inline=True)
    embed.set_footer(
        text="If you have any questions, suggestions or bug reports, please join our support Discord Server: https://discord.gg/WJECeuXSej",
        icon_url=f"{bot.user.avatar_url}")
    await ctx.author.send(embed=embed)


@bot.command()
async def staff(ctx):
    embed = discord.Embed(title="**Our staff**", description="\n", colour=0xe74c3c)
    embed.add_field(name="TheForeskinCollector", value=f"**Founder / Developer**", inline=False)
    embed.add_field(name="Kartoffel", value=f"**Donator of 2 Euro/Month**", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    try:
        embeds = []
        embed = discord.Embed(title=f"Help Overview", colour=0x7289da)
        #embed.add_field(name=f"<:cautionwarning:957442062838558761> DOWNTIME <:cautionwarning:957442062838558761>", value=f"Expected Downtime!\nGet more Info's on [our Website!](https://www.admin-helper.tk/downtime.html)", inline=False)
        embed.add_field(name=f"Page 1", value=f"Help Overview", inline=False)
        embed.add_field(name=f"Page 2", value=f"All Non-Moderation commands", inline=False)
        embed.add_field(name=f"Page 3", value=f"Most Used Commands", inline=False)
        embed.add_field(name=f"Page 4", value=f"Fun Commands", inline=False)
        embed.add_field(name=f"Page 5", value=f"All Moderation Commands", inline=False)
        embed.add_field(name=f"Page 6", value=f"Whitelisted Commands", inline=False)
        embed.add_field(name=f"Page 7", value=f"Slash Commands", inline=False)
        embed.add_field(name=f"Page 8", value=f"Support", inline=False)
        embed.add_field(name=f"Invite Me Over", value=f"[Admin Helper](https://www.admin-helper.tk/)", inline=False)
        embed.set_footer(text="New website is planed!")
        embeds.append(embed)
        embed = discord.Embed(
            title="All commands:",
            description="", colour=0x7289da)
        embed.add_field(name="-insult [@user]",
                        value="Insult someone.",
                        inline=True)
        embed.add_field(name="-afk [reason] [time]",
                        value="Go afk for xy minutes.",
                        inline=True)
        embed.add_field(name="-invisping [@user] [text]",
                        value="Make an Invisible ping. Only PC user will see it!",
                        inline=True)
        embed.add_field(name="-gayquiz",
                        value="Take an gay quiz to prove your innocence ",
                        inline=True)
        embed.add_field(name="-8ball [question]",
                        value="Answers your question.",
                        inline=True)
        embed.add_field(name="-coinflip",
                        value="Flips a coin.",
                        inline=True)
        embed.add_field(name="-servercount",
                        value="See in how many Server Admin Helper is in.", inline=True)
        embed.add_field(name="-serverinfo",
                        value="Get informations about the server.", inline=True)
        embed.add_field(name="-whois [@user]",
                        value="Get informations about that user.", inline=True)
        embed.add_field(name="-membercount",
                        value="See how many member your server has.", inline=True)
        embed.add_field(name="-avatar [@user]",
                        value="Get the avatar of the user.", inline=True)
        embed.add_field(name="-meme",
                        value="See a random meme.", inline=True)
        embed.add_field(name="-gayrate [@user]",
                        value="See how gay the you or the Person is.", inline=True)
        embed.add_field(name="-pickup [@user]",
                        value="Get a pickup line.", inline=True)
        embed.add_field(name="-bugreport",
                        value="Fill out a form to send a bug-report", inline=True)
        embed.set_footer(text="Next page are Most used Commands")
        embeds.append(embed)
        embed = discord.Embed(
                        title="Most used Commands:",
                        description="", colour=0x7289da)
        embed.add_field(name="-gayrate [@user]", value="See how Gay you or another Person is.", inline=False)
        embed.add_field(name="-whois [@user]", value="Get informations about that user.", inline=False)
        embed.add_field(name="-servercount", value="See in how many Server Admin Helper is in.", inline=False)
        embed.set_footer(text="Next page are Fun Commands!")
        embeds.append(embed)
        embed = discord.Embed(
            title="Fun Commands:",
            description="", colour=0x7289da)
        embed.add_field(name="-meme", value="Get a random Meme.", inline=False)
        embed.add_field(name="-color [Hex]", value="See what color that HEX code is.", inline=False)
        embed.add_field(name="-translate [Language e.g de, fr, en] [Text]", value="Translate your text.", inline=False)
        embed.add_field(name="-morse [Text]", value="Make your text into Morse-code.", inline=False)
        embed.add_field(name="-wyr", value="Would you rather.", inline=False)
        embed.add_field(name="-chatbot [Text]", value="Chat with the bot.", inline=False)
        embed.add_field(name="-gayrate [@user]", value="See how Gay you or the Person is.", inline=False)
        embed.add_field(name="-joke", value="Get a random Joke.", inline=False)
        embed.add_field(name="-youtube [@user] [Text]", value="Publish a Fake YouTube comment.", inline=False)
        embed.set_footer(text="Next page are Moderation Commands!")
        embeds.append(embed)
        embed = discord.Embed(
            title="Moderation Commands:",
            description="", colour=0x7289da)
        embed.add_field(name="-ban [@user] [reason]", value="Ban the user.", inline=False)
        embed.add_field(name="-kick [@user] [reason]", value="Kick the user.", inline=False)
        embed.add_field(name="-slowmode [number]", value="Enable or Disable Slow mode.", inline=False)
        embed.add_field(name="-mute [@user] [reason]", value="Mute the user.", inline=False)
        embed.add_field(name="-unmute [@user] [reason]", value="Unmute the muted user.", inline=False)
        embed.add_field(name="-warn [@user] [reason]", value="Warn the user.", inline=False)
        embed.add_field(name="-prefix [prefix]", value="Make a new Prefix for the Server.", inline=False)
        embed.add_field(name="-poll [Question]", value="Make a poll for the Server.", inline=False)
        embed.add_field(name="-nick [@user] [nickname]", value="Nick the user.", inline=False)
        embed.add_field(name="-addpartner [invite link]", value="Want to find partners? Add your server.", inline=False)
        embed.add_field(name="-partners", value="Want to find a partner?", inline=False)
        embed.set_footer(text="Next page are Whitelisted Commands!")
        embeds.append(embed)
        embed = discord.Embed(
                        title="Whitelisted Commands:",
                        description="", colour=0x7289da)
        embed.add_field(name="-sudo [@user] [Text]", value="Send a message as the user.", inline=False)

        embed.set_footer(text="Next page is Support!")
        embeds.append(embed)
        embed = discord.Embed(
                        title="Slash Commands:",
                        description="", colour=0x7289da)
        embed.add_field(name="/chatbot [text]", value="Chat with the bot. Only you can see his responses.", inline=False)
        embed.add_field(name="/gayrate [@user]", value="See how gay you or the Person is.", inline=False)
        embed.add_field(name="/insult [@user]", value="Insult you or a Person.", inline=False)
        embed.add_field(name="/pickup [@user]", value="Get a pickup line.", inline=False)
        embed.add_field(name="/prefix [New Prefix]", value="Change the Prefix of the Server.", inline=False)
        embed.add_field(name="/statuses", value="See the status meanings of the bot.", inline=False)
        embed.set_footer(text="More questions/problems? Use -bugreport")
        embeds.append(embed)
        embed = discord.Embed(
                        title="Support:",
                        description="", colour=0x7289da)
        embed.add_field(name="Sudo Command Whitelisting", value="To get access to the Sudo command please use the -bugreport command.", inline=True)
        embed.add_field(name="Sudo Command Not Working?", value="The Sudo Command has a Maximum of 10 Uses in a Channel.\nThis can't be fixed due to Discord", inline=True)
        embed.add_field(name="-support", value="Get a Server invite to our Support Server.", inline=False)
        embed.add_field(name="-suggest", value="Suggest a command to Admin Helpers staff.", inline=False)
        embed.add_field(name="-credits", value="Credits/Contributors.", inline=False)
        embed.add_field(name="-partners", value="Admin Helper's partners.", inline=False)
        embed.add_field(name="-discovery", value="Admin Helper's Discovery status.", inline=False)
        #embed.add_field(name="-servercount", value="See in how many Server Admin Helper is in.")
        embed.set_footer(text="More questions/problems? Use -bugreport")
        embeds.append(embed)

        pages = 8
        cur_page = 1
        message1 = await ctx.send(f"Page {cur_page} of {pages}")
        message = await ctx.send(embed=embeds[cur_page-1])
        await message.add_reaction("◀")
        await message.add_reaction("▶")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀", "▶"]
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check=check)
                if str(reaction.emoji) == "▶" and cur_page < pages:
                    cur_page += 1
                    await message1.edit(content=f"Page {cur_page}/{pages}")
                    await message.edit(embed=embeds[cur_page-1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀" and cur_page > 1:
                    cur_page -= 1
                    await message1.edit(content=f"Page {cur_page} of {pages}")
                    await message.edit(embed=embeds[cur_page-1])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
            except:
                pass
            #except:
            #    await ctx.send("Something went wrong here!")
    except ctx.channel.type == discord.ChannelType.private:
        await ctx.send("Please use this command in a server")

filepwdlist1 = open("10-million-password-list-top-1000000.txt", "r")
lines = filepwdlist1.readlines()

@bot.command(aliases = ["Password", "Passwort", "passwort", "pw", "PW", "Pw"])
async def password(ctx, *, password):
    embed = discord.Embed(title="Checking...")
    loading_message = await ctx.send(embed=embed)
    try:
        if password + "\n" in lines:
            embed=discord.Embed(title="Password Checker!", color=0xff0000)
            embed.set_author(name="Admin Helper", icon_url="https://cdn.discordapp.com/avatars/930842036360319067/d9c260413a71f14d0c01e4b810dc5067.webp")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/877796755234783273/879311068097290320/PngItem_1526969.png")
            #embed.add_field(name=f"Your Passoword", value=f"{password}", inline=False)
            embed.add_field(name=f"Safety", value=f"I've seen this Password so many times!", inline=False)
            #embed.set_footer(text=f"Requested by {ctx.author.name}")
            await loading_message.delete()
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Password Checker!", color=0xff0000)
            embed.set_author(name="Admin Helper", icon_url="https://cdn.discordapp.com/avatars/930842036360319067/d9c260413a71f14d0c01e4b810dc5067.webp")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/877796755234783273/879311068097290320/PngItem_1526969.png")
            #embed.add_field(name=f"Your Passoword", value=f"{password}", inline=False)
            embed.add_field(name=f"Safety", value=f"I haven't seen that Password anywhere yet!", inline=False)
            #embed.set_footer(text=f"Requested by {ctx.author.name}")
            await loading_message.delete()
            await ctx.send(embed=embed)

    except Exception as e:
        embed2=discord.Embed(title=":red_square: Oopsie woopsie!", description="I dropped the soap and forgot what you asked me 😖! ", color=0xff0000)
        embed2.set_author(name="Admin Helper", icon_url="https://cdn.discordapp.com/avatars/930842036360319067/d9c260413a71f14d0c01e4b810dc5067.webp")
        embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/877796755234783273/879298565380386846/sign-red-error-icon-1.png")
        embed2.add_field(name="Error:", value=f"{e}", inline=False)
        #embed2.set_footer(text=f"Requested by {ctx.author.name}")
        await loading_message.delete()
        await ctx.send(embed=embed2)

import string

#import uuid
#
#
#def randompas(string_length=27):
#
#    random = str(uuid.uuid4())
#    random = random.upper()
#    random = random.lower()
#    random = random.replace("-", "$" or "^" or "!")
#    return random[0:string_length]

@bot.command()
async def passgen(ctx):
    randompas = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in
                      range(16)])
    #print(randompas(27))
    embed = discord.Embed(title="Password Generator", description=randompas, color=0x0055ff)
    embed.set_image(url="https://cdn.discordapp.com/attachments/828715470516912158/962073358923599902/password.PNG")
    await ctx.author.send(embed=embed)

@bot.command(aliases = ["addpartner"])
@commands.cooldown(1, 43200, commands.BucketType.guild)
#@commands.cooldown(1, 43200, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def _partner(ctx, invite = None):
    try:
        if invite is None:
            embed = discord.Embed(title=f"Failed!", description=f"Please provide an Invite link that is also Infinite!", colour=0xe74c3c)
            embed.set_footer(text=f"Servers that are NSFW based or gore based or Violating TOS and/or Guidelines will be removed and reported to Discord!")
            await ctx.send(embed=embed)
        else:
            async with aiofiles.open(f'partner.txt', mode="a") as file:
                await file.write(f"\n{invite}")
            embed = discord.Embed(title=f"Success!", description=f"Other servers can now find your Server!", colour=0x1f8b4c)
            embed.add_field(name=f"Rules!", value=f"Servers that are NSFW based or gore based or Violating TOS and/or Guidelines will be removed and reported to Discord!", inline=False)
            embed.add_field(name="Please keep in mind", value="You can not remove this invite manually!", inline=False)
            embed.add_field(name=f"Did an oopsie?", value="You added your server even tho they're against the Rules? Use -bugreport and say the following;\n"
                                                          "\"I added our server as Partner! It contains ... we wish to remove the following server invite! *__Your server invite__*\"", inline=False)
            embed.set_footer(text="You can 'Upvote' your server every 12 Hours!")
            await ctx.send(embed=embed)
    except PermissionError:
        embed = discord.Embed(title=f"", description=f"You dont have permissions to perform this command.")
        await ctx.send(embed=embed)

@bot.command()
#@commands.cooldown(1, 5, commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def partners(ctx):
     with open(f'partner.txt', "r") as f:
        read = f.read()
        array = read.split('\n')
        partner = random.choice(array)
        await ctx.send(f"This server is currently searching for a Partner!: {partner}")

#@bot.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.CommandOnCooldown):
#        embed = discord.Embed(title=f"Calm down buddy!", description=f"You need to wait {round(error.retry_after, 2)} Seconds before retrying! About 12 Hours 😱😱")
#        await ctx.send(embed=embed)

message_counter = 2

@bot.listen()
async def on_message(message):
    global message_counter
    message_counter += 2


@bot.command()
@commands.has_permissions(administrator=True)
async def admin(ctx):
    embed = discord.Embed(title=f"<:cautionwarning:957442062838558761> We have removed this command. Please use `-help`.", description=f"", colour=0xe74c3c)
    await ctx.reply(embed=embed)


@bot.command()
async def whois(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    roles = [role for role in member.roles]
    embed = discord.Embed(timestamp=ctx.message.created_at,
                          title=f"User Info", colour=member.colour)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(name="Display Name:", value=member.display_name, inline=False)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]), inline=False)
    embed.add_field(name="Highest Role:", value=member.top_role.mention, inline=False)
    await ctx.send(embed=embed)

#@bot.command()
#async def emoji(ctx, emoji):
#    embed = discord.Embed(timestamp=ctx.message.created_at,
#                          title=f"Emoji Info", colour=ctx.author.colour)
#    #embed.set_thumbnail(url=emoji)
#    embed.set_footer(text=f"Requested by {ctx.author}")
#
#    embed.add_field(name="ID:", value=emoji.id, inline=False)
#    embed.add_field(name="Display Name:", value=emoji, inline=False)
#    await ctx.send(embed=embed)


@bot.command()
async def joindate(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(title="", description=f'{ctx.author.mention}', color=0x5865f2)
        embed.add_field(name="You joined the Server On:", value=ctx.author.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="", description=f'{member.mention}', color=0x5865f2)
        embed.add_field(name=f"Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        await ctx.reply(embed=embed)


@bot.command()
async def cep(ctx, message):
    embed = discord.Embed(title="", description=f'Created: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    await ctx.reply(embed=embed)



@bot.command()
async def amongus(ctx):
    await ctx.send(f'i will kill you ', tts=True)


@bot.command()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    description = str(ctx.guild.description)
    embed = discord.Embed(
        title=name + " Server Information",
        color=discord.Color.purple()
    )
    if region is None:
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Server Info", value=description, inline=True)
        embed.add_field(name="Region", value='None', inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        await ctx.send(embed=embed)
    else:
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Server Info", value=description, inline=True)
        embed.add_field(name="Region", value='None', inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        await ctx.send(embed=embed)


@bot.command()
async def support(ctx):
    embed = discord.Embed(title="For support please join our Discord Server", description="", color=discord.Color.red())
    embed.add_field(name="__Discord__", value="[Our Discord](https://discord.gg/wY3Q4PJHJk)", inline=False)
    #embed.add_field(name='__Website__', value='[Our Website](http://127.0.0.1:5500/index.html)',inline=False)
    await ctx.author.send(embed=embed)


@bot.command(aliases = ["sc", "servers"])
async def servercount(ctx):
    embed = discord.Embed(title="", description="", colour=0xe74c3c)
    botGuilds = str(len(bot.guilds))
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
    embed.add_field(name="Server Count", value=botGuilds, inline=True)
    embed.add_field(name="User count", value=f"{members}", inline=False)
    embed.add_field(name="Do us a favour", value=f"[Vote us up](https://discordbotlist.com/bots/admin-helper/upvote)", inline=False)
    await ctx.send(embed=embed)


bot.uptime = 0

@tasks.loop(minutes=1)
async def uptime():
    bot.uptime += 1


response_list = ping('8.8.8.8', size=40, count=10)
@bot.command()
async def about(ctx):
    embed = discord.Embed(title="About me!", description="", colour=0x7289da)
    embed.add_field(name="Languages I support", value=f"Currently I only support English <:ameritan:966219934386503701>", inline=False)
    embed.add_field(name="Programming language", value=f"Python (3.9), discord.py (1.7.3) <:1887_python:957334552613908550>", inline=False)
    embed.add_field(name=f"What am I?", value=f"I'm a multipurpose bot, you can use me for `Moderation`, `Fun` or something else.", inline=False)
    embed.add_field(name=f"Where was I created?", value=f"I was made in Germany near Munich.", inline=False)
    embed.add_field(name=f"When was I created?", value=f"Wed, 12 January 2022, 03:13 PM UTC", inline=False)
    embed.add_field(name=f"How many commands do I offer?", value=f"{str(len(bot.all_commands))}", inline=False)
    embed.add_field(name=f"Messages sent\n(Since Uptime)", value=f"***{message_counter}***", inline=True)
    embed.add_field(name=f"Uptime", value=f"***{bot.uptime} Minutes***", inline=True)
    embed.add_field(name=f"Ping", value=f"{response_list.rtt_avg_ms} ms", inline=True)
    embed.set_footer(text=f"We cant see what you write!")
    await ctx.send(embed=embed)

@bot.command()
async def stats(ctx):
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
    botGuilds = str(len(bot.guilds))
    embed = discord.Embed(title="Stats of Admin Helper", description="")
    embed.add_field(name="Servercount", value=f"{botGuilds}", inline=False)
    embed.add_field(name="Membercount", value=f"{members}", inline=False)
    embed.add_field(name="Uptime", value=f"{bot.uptime} Minutes", inline=False)
    embed.add_field(name="Ping", value=f"{response_list.rtt_avg_ms} ms", inline=False)
    embed.add_field(name="Messages sent", value=f"{message_counter}", inline=False)
    await ctx.reply(embed=embed)


@bot.command()
async def membercount(ctx):
    color = discord.Color.purple()
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    embed = discord.Embed(
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Members", value=memberCount, inline=True)
    timestamp = ctx.message.created_at,
    await ctx.send(embed=embed)


@bot.command(aliases=["av"])
async def avatar(ctx, *, member: discord.Member = None):
    member = member or ctx.author
    if ctx.guild is None:
        embed = discord.Embed(title=f"My avatar", color=0x5865f2)
        # embed.set_author(name=f"{member.display_name}", icon_url=str(member.avatar_url))
        embed.set_image(url="https://cdn.discordapp.com/avatars/930842036360319067/d9c260413a71f14d0c01e4b810dc5067.webp")
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(title=f"{member.display_name}'s avatar", color=0x5865f2)
    #embed.set_author(name=f"{member.display_name}", icon_url=str(member.avatar_url))
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)


# memes
@bot.command(aliases = ["MEME", "mEME", "Meme", "memes", "mEMES", "MEMES"])#pass_context=True
async def meme(ctx):
    embed = discord.Embed(title="", description="")
    color = discord.Color.purple()

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


answer8 = ["My final answer is no", "Yes", "Definitely yes", "Nope", "Try asking me later", "I'm not gonna say that", "I don't know", "My final answer is yes", "Definitely no"]
@bot.command(aliases = ["8ball"])
async def _ball(ctx, *, question = None):
    if question is None:
        em = discord.Embed(title=f"Try using it again but ask me a question this time", description="", color=0x992d22)
        await ctx.send(embed=em)
    else:
        em = discord.Embed(title="8Ball", description=f"**Question**: {question}\n**Answer**: {random.choice(answer8)}", color=0x0055ff)
       #em.add_field(name=f"Question:", value=f"{question}", inline=True)
       #em.add_field(name=f"Answer", value=f"{random.choice(answer8)}", inline=False)
        em.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=str(ctx.author.avatar_url))
        em.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=em)


#bot.warnings = {}
#@bot.event
#async def on_ready():
#
#    for guild in bot.guilds:
#        bot.warnings[guild.id] = {}
#
#        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
#            pass
#
#        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
#            lines = await file.readlines()
#
#            for line in lines:
#                data = line.split(" ")
#                member_id = int(data[0])
#                admin_id = int(data[1])
#                reason = " ".join(data[2:]).strip("\n")
#
#                try:
#                    bot.warnings[guild.id][member_id][0] += 1
#                    bot.warnings[guild.id][member_id][1].append((admin_id, reason))
#
#                except KeyError:
#                    bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]
#
#
#@bot.event
#async def on_guild_join(guild):
#    bot.warnings[guild.id] = {}
#
#
#@bot.command()
#@commands.has_permissions(administrator=True)
#async def warn(ctx, member: discord.Member = None, *, reason=None):
#    if member is None:
#        return await ctx.send("The provided member could not be found or you forgot to provide one.")
#
#    if reason is None:
#        return await ctx.send("Please provide a reason for warning this user.")
#
#    try:
#        first_warning = False
#        bot.warnings[ctx.guild.id][member.id][0] += 1
#        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))
#
#    except KeyError:
#        first_warning = True
#        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]
#
#    count = bot.warnings[ctx.guild.id][member.id][0]
#
#    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
#        await file.write(f"{member.id} {ctx.author.id} {reason}\n")
#
#    embed = discord.Embed(title=f"", description=f"***You have been warned in {ctx.guild.name} by {ctx.author.top_role.mention} {ctx.author.mention}. Reason: {reason}.***\nThis is your {count} {'warning' if first_warning else 'warning'}.", colour=discord.Colour.red())
#    await member.send(embed=embed)
#
#    embed = discord.Embed(title=f"", description=f":white_check_mark: ***Warned {member.mention}.***\n***This is his {count} {'warning' if first_warning else 'warning'}.***", colour=discord.Colour.red())
#    await ctx.send(embed=embed)
# Backup of kick cmd

# @kick.error
# async def kick_error(error, ctx):
# if isinstance(error, commands.MissingPermissions):
#  owner = ctx.guild.owner
#  direct_message = await owner.create_dm()
#  await direct_message.send("Missing Permissions")

#@bot.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.reply(f"You cant do that with the air silly!")
#        await ctx.reply(f"You will need to provide something to me!")


#@bot.command(name="ping")
#async def ping(ctx: commands.Context):
#    await ctx.send(f"{round(bot.latency * 1000)}ms")

# MODERATIONNNNNNNNNNNNNNNNN


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=False)
        await member.add_roles(mutedRole, reason=reason)
        embed = discord.Embed(title="", description=f"<:GreenTick:957279366499409950> ***{member.name} Was muted for the reason: `{reason}`***",
                              colour=0x992d22)
        await ctx.send(embed=embed)
        embed = discord.Embed(title="", description=f'<:cautionwarning:957442062838558761> ***You were muted in {guild.name}. Reason: `{reason}`***', colour=0x992d22)
        await member.send(embed=embed)

@bot.command()
async def furry(ctx):
    await ctx.send(
        f'{ctx.author.mention} Shame your self: https://cdn.discordapp.com/attachments/935989994735169546/943308867322921000/VideoGlitch_20220205_183023606.mp4')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedRole)
        embed = discord.Embed(title="", description=f"<:GreenTick:957279366499409950> ***Unmuted {member.name}.***", colour=0x2ecc71)
        await ctx.send(embed=embed)
        embed = discord.Embed(title="", description=f'<:GreenTick:957279366499409950> ***You were unmuted in {ctx.guild.name}***.', colour=0x992d22)
        await member.send(embed=embed)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    embed = discord.Embed(title="", description=f'***{limit} Messages Purged by {ctx.author.mention}.***',
                          delete_after=20, colour=0x992d22)
    await ctx.send(embed=embed)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
 if seconds == 0:
     await ctx.channel.edit(slowmode_delay=0)
     embed = discord.Embed(title="",
                           description=f"<:GreenTick:957279366499409950> ***Disabled the slowmode delay in this channel!***",
                           colour=0x992d22)
     await ctx.send(embed=embed)
 else:
    await ctx.channel.edit(slowmode_delay=seconds)
    embed = discord.Embed(title="", description=f"<:GreenTick:957279366499409950> ***Set the slowmode delay in this channel to {seconds} seconds!***",
                          colour=0x992d22)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(title="", description=f"<:GreenTick:957279366499409950> ***{member.name} was banned.***", delete_after=10,
                              colour=0x992d22)
        await ctx.send(embed=embed)
        embed = discord.Embed(title="", description=f"<:cautionwarning:957442062838558761> ***You were banned in {ctx.guild.name}. Reason: `{reason}`.***",
                              colour=0x992d22)
        await member.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, user: discord.Member = None, *, reason="> No reason provided"):
        async with aiofiles.open(f'{ctx.guild.id}.txt', mode="a") as file:
            await file.write(f"**Admin: {ctx.author.mention}** warned *{user.mention}* for the reason: ***{reason}***\n")
        embed = discord.Embed(title="", description=f"<:cautionwarning:957442062838558761> ***You were warned in {ctx.guild.name}. Reason: `{reason}`***",
                              colour=0x992d22)
        await user.send(embed=embed)
        embed = discord.Embed(title="", description=f"<:GreenTick:957279366499409950> ***{user.name} was warned.***", delete_after=25,
                              colour=0x992d22)
        await ctx.send(embed=embed)

@bot.command(aliases=["warnings", "Warnings", "Warns"])
@commands.has_permissions(administrator=True)
async def warns(ctx, member: discord.Member):
    with open(f"{ctx.guild.id}.txt", "r") as file:
        file_lines = file.readlines()
        description = ""
        for file_line in file_lines:
            if member.mention in file_line:
                description += str(file_line)
        if len(description) > 0:
            embed = discord.Embed(description=description)
            await ctx.send(embed=embed)
            return
        if member.mention not in file_lines:
            embed = discord.Embed(title="Hmmm!", description=f"Looks like there are no warnings for {member.mention}!")
            return await ctx.send(embed=embed)

            #if member.mention not in line:
            #    embed = discord.Embed(title="Hmmm!", description=f"Looks like there are no warnings for {member.mention}!")
            #    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(title="", description=f"<:GreenTick:957279366499409950> ***{member.name} was kicked.***", delete_after=10,
                              colour=0x992d22)
        await ctx.send(embed=embed)
        embed = discord.Embed(title="", description=f"<:GreenTick:957279366499409950> ***You were kicked from {ctx.guild.name}. Reason: `{reason}`.***", colour=0x992d22)
        await member.send(embed=embed)


# backup of nick cmd

@bot.command()
@commands.has_permissions(change_nickname=True)
async def nick(ctx, member: discord.Member, *, nick=None):
    if nick is None:
     embed = discord.Embed(title="", description=f'This cant be blank silly.', colour=0x992d22)
     await ctx.reply(embed=embed)
    else:
     try:
        await member.edit(nick=nick)
        embed = discord.Embed(title="", description=f'<:GreenTick:957279366499409950> Nickname changed.', colour=0x0000ff)
        await ctx.reply(embed=embed)
     except:
         embed = discord.Embed(title="", description=f'<:cautionwarning:957442062838558761> **An error has occurred!**\n**Here are possible reasons why it may didn\'t work**:\n``Person has the same role as the bot.``\n``The user is the owner of the bot.``\n``Me and/or you don\'t have the permissions to perform this command.``', colour=0x992d22)
         await ctx.reply(embed=embed)


# IDK?




coin = ['Heads', 'Tails']


@bot.command()
async def coinflip(ctx):
 embed = discord.Embed(title="", description="The coin has been flipped:\n**{}**".format(random.choice(coin)), color=0x0000ff)
 await ctx.send(embed=embed)

#
#@bot.command()
#async def staff(ctx):
#    embed = discord.Embed(title=f"", description=f'Meet our [Staff](https://www.admin-helper.tk/) here soon!', colour=0x0000ff)
#    await ctx.send(embed=embed)

#@bot.event
#async def on_member_join(member):
#    #channel = discord.utils.get(member.guild.channels, name="general")
# if member.guild.id == 935312744217989150:
#    embed=discord.Embed(title=f"", description=f"Welcome to **{member.guild.name}**, {member.mention}!", color=0x0000ff)
#    await member.send(embed=embed)
#
#@bot.event
#async def on_member_remove(member):
#    #channel = discord.utils.get(member.guild.channels, name="general")
# if member.guild.id == 935312744217989150:
#    embed=discord.Embed(title=f"", description=f"Bye! {member.mention}!", color=0x0000ff)
#    await member.send(embed=embed)
#
#@bot.event
#async def on_member_join(member):
#    #channel = discord.utils.get(member.guild.channels, name="general")
# if member.guild.id == 954827098789404702:
#    embed=discord.Embed(title=f"", description=f"Welcome to **{member.guild.name}**, {member.mention}!", color=0x0000ff)
#    await member.send(embed=embed)
#
#@bot.event
#async def on_member_remove(member):
#    #channel = discord.utils.get(member.guild.channels, name="general")
# if member.guild.id == 954827098789404702:
#    embed=discord.Embed(title=f"", description=f"Bye! {member.mention}!", color=0x0000ff)
#    await member.send(embed=embed)

@bot.command()
async def invisping(ctx, member: discord.Member, *, text):
    await ctx.send(f"{text}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| ||{member.mention}")

@bot.command(aliases=["et"])
@commands.is_owner()
async def embedthis(ctx, *, reason):
    if reason is None:
          await ctx.channel.purge(limit=1)
          embed = discord.Embed(title=f"", description=f"Please give me an Message to embed.", colour=ctx.author.color)
          await ctx.send(embed=embed)
    else:
        try:
          await ctx.channel.purge(limit=1)
          embed = discord.Embed(title=f"", description=f"{reason}", colour=ctx.author.color)
          await ctx.send(embed=embed)
        except commands.MissingPermissions:
            await ctx.channel.purge(limit=1)
            embed = discord.Embed(title=f"Hey there {ctx.author.name}!", description=f"Only my daddy can use this command!", colour=ctx.author.color)
            await ctx.send(embed=embed)

import datetime

@bot.command(aliases=["POLL", "pOLL", "Poll"])
@has_permissions(administrator=True)
async def poll(ctx, *, question, option1=None, option2=None):
  if option1==None and option2==None:
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title=f"Poll:", description=f"**{question}**\n\n**<:3556orvoteyes:953351940975255592> = Yes**\n**<:4662orvoteno:953351940635500585> = No**")
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f'Poll by {ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
    message = await ctx.send(embed=embed)
    await message.add_reaction('<:3556orvoteyes:953351940975255592>')
    await message.add_reaction('<:4662orvoteno:953351940635500585>')
  elif option1==None:
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title=f"Poll:", description=f"**{question}**\n\n**<:3556orvoteyes:953351940975255592> = {option1}**\n**<:4662orvoteno:953351940635500585> = No**")
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f'Poll by {ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
    message = await ctx.send(embed=embed)
    await message.add_reaction('<:3556orvoteyes:953351940975255592>')
    await message.add_reaction('<:4662orvoteno:953351940635500585>')
  elif option2==None:
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title=f"Poll:", description=f"**{question}**\n\n**<:3556orvoteyes:953351940975255592> = Yes**\n**<:4662orvoteno:953351940635500585> = {option2}**")
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f'Poll by {ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
    message = await ctx.send(embed=embed)
    await message.add_reaction('<:3556orvoteyes:953351940975255592>')
    await message.add_reaction('<:4662orvoteno:953351940635500585>')
  else:
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title=f"Poll:", description=f"**{question}**\n\n**<:3556orvoteyes:953351940975255592> = {option1}**\n**<:4662orvoteno:953351940635500585> = {option2}**")
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f'Poll by {ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
    message = await ctx.send(embed=embed)
    await message.add_reaction('<:3556orvoteyes:953351940975255592>')
    await message.add_reaction('<:4662orvoteno:953351940635500585>')

#@bot.command(pass_context=True)
#async def bugreport(ctx, *, text = None):
#    if isinstance(ctx.channel, discord.DMChannel):
#        if text is None:
#            await ctx.author.send("```Usage: -bugreport [content]```")
#        else:
#            auser = bot.get_user(int(834530511790538763))
#            await auser.send("<@834530511790538763> **{}**({}) : {}".format(ctx.author, ctx.author.id, text))
#            await ctx.author.send("**INFO:** A message was sent to the bot developers.")
 #   else:
 #       await ctx.message.delete()


#@bot.command()
#async def ad(ctx):
# blacklist = []
# if blacklist:
#     await ctx.send("test")
# else:
#    embed = discord.Embed(title=f"", description=f'')
#    color = discord.Color.purple()
#    embed.set_image(url="https://media.giphy.com/media/UPUVyGoW8PUKZPA3F8/giphy.gif")
#    embed.set_footer(text="https://discord.gg/WJECeuXSej", )
#    await ctx.send(embed=embed)


@bot.command()
async def gayrate(ctx, member: discord.Member = None):
    if member == None:
        embed = discord.Embed(title=f"", description=f'', colour=0x992d22)
        embed.add_field(name=f"Gayrate:", value=f"{random.randint(0, 100)}%")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"", description=f'', colour=0x992d22)
        embed.add_field(name=f"Gayrate:", value=f"{random.randint(0, 100)}%")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Request for {member.display_name}', icon_url=f"{member.avatar_url}")
        await ctx.send(embed=embed)


size = ["Meter", "Millimeter", "Feet", "Miles", "Centimeter"]

@bot.command()
async def ballsize(ctx, member: discord.Member = None):
    if member == None:
        embed = discord.Embed(title=f"", description=f'', colour=0x992d22)
        embed.add_field(name=f"Ballsize", value=f'{random.randint(0, 100)} {random.choice(size)}')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"", description=f'', colour=0x992d22)
        embed.add_field(name=f"Ballsize", value=f'{random.randint(0, 100)} {random.choice(size)}')
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Request for {member.display_name}', icon_url=f"{member.avatar_url}")
        await ctx.send(embed=embed)


# FUN COMMANDS

@bot.command()
@commands.is_owner()
async def rr(ctx, *, text): # role1, role2, role3,
        embed = discord.Embed(title="Reaction Roles for ShitPost LORE", description=f"{text}")
        message = await ctx.send(embed=embed)
        role1 = '🌈'
        role2 = '🏁'
        role3 = '💩'

        await message.add_reaction(role1)
        await message.add_reaction(role2)
        await message.add_reaction(role3)

        def check(reaction, user):
            return user == user and str(
                reaction.emoji) in [role1, role2, role3]


        try:
            reaction, user = await bot.wait_for("reaction_add", check=check)

            if str(reaction.emoji) == role1:
                role1 = discord.utils.get(bot.get_guild(971465291404029993).roles, id="972550682144047114")
                await reaction.author(role1)

            if str(reaction.emoji) == role2:
                role2 = discord.utils.get(bot.get_guild(971465291404029993).roles, id="972280443003076738")
                await reaction.author(role2)

            if str(reaction.emoji) == role3:
                role2 = discord.utils.get(bot.get_guild(971465291404029993).roles, id="972550873555275786")
                await reaction.author(role3)

        except on_command_error:
            await ctx.send("There was an error!")


@bot.command()
async def sex(ctx, member: discord.Member):
    if member is ctx.author:
        await ctx.send(f"You cant do that with your self silly.")
    else:
        message = await ctx.send(f"{ctx.author.mention} wants to have sexual intercourse with {member.mention}")
        thumb_up = '👍'
        thumb_down = '👎'

        await message.add_reaction(thumb_up)
        await message.add_reaction(thumb_down)

        def check(reaction, user):
            return user == member and str(
                reaction.emoji) in [thumb_up, thumb_down]

        member = member

        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=80.0, check=check)

            if str(reaction.emoji) == thumb_up:
                await ctx.send(f'Yay! {ctx.author.mention} will love to hear that!')

            if str(reaction.emoji) == thumb_down:
                await ctx.send(f'Sorry {ctx.author.mention}! But it wont look good for you.')

        except on_command_error:
            await ctx.send("There was an error!")


@bot.command()
async def pleasewhereismydad(ctx):
    await ctx.send(f'> He left you on your birth so he doesn\'t need to see your ugly face')


@bot.command()
@commands.has_permissions(embed_links=True)
async def tf2(ctx):
    await ctx.send(
        f'> https://cdn.discordapp.com/attachments/894917452922765343/918255504688574534/87-3.mp4 {ctx.author.mention}')


answers = ["Admin Helper is the best Bot in the history of Discord.", "He decided water-skiing on a frozen lake wasn’t a good idea.", "It was a really good Monday for being a Saturday.", "He decided to fake his disappearance to avoid jail.", "8% of 25 is the same as 25% of 8 and one of them is much easier to do in your head.", "He didn't understand why the bird wanted to ride the bicycle.", "The fox is not a rabbit."]


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def type(ctx):
    starttime = time.time()
    answer = random.choice(answers)
    timer = 35
    embed = discord.Embed(title="", description=f'You have {timer} seconds to type: "***``{answer}``***"', colour=0x0000ff)
    await ctx.send(embed=embed)

    def is_correct(msg):
        return msg.author == ctx.author

    try:
        guess = await bot.wait_for('message', check=is_correct, timeout=timer)
    except asyncio.TimeoutError:
        embed = discord.Embed(title="", description=f"You took too long to answer me!", colour=0x0000ff)
        return await ctx.send(embed=embed)

    if guess.content == answer:
        fintime = time.time()
        total = fintime - starttime
        embed = discord.Embed(title="You got it right! ", description=f"You took {round(total)} seconds!", colour=0x0000ff)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="", description=f"That wasn't quite right, or was it?", colour=0x0000ff)
        await ctx.send(embed=embed)
        fintime = time.time()
        total = fintime - starttime
        embed = discord.Embed(title="You got it wrong! ", description=f"But you took {round(total)} seconds!", colour=0x0000ff)
        await ctx.send(embed=embed)

@bot.command()
async def yomama(ctx, member: discord.Member=None):
 if member:
    with open("slurs.txt", "r") as f:
            read = f.read()
            array = read.split('\n')
            quote = random.choice(array)
            async with ctx.typing():
                await asyncio.sleep(2)
            await ctx.reply(f"{member.mention} {quote}")
 else:
     with open("slurs.txt", "r") as f:
         read = f.read()
         array = read.split('\n')
         quote = random.choice(array)
         async with ctx.typing():
             await asyncio.sleep(2)
         await ctx.reply(f"{ctx.author.mention} {quote}")


@bot.command()
async def pickup(ctx, member: discord.Member=None):
    if member:
       with open("pickup.txt", "r") as f:
            read = f.read()
            array = read.split('\n')
            quote = random.choice(array)
            await ctx.reply(f"{member.mention} {quote}")
    else:
        with open("pickup.txt", "r") as f:
            read = f.read()
            array = read.split('\n')
            quote = random.choice(array)
            await ctx.reply(f"{quote}")


@bot.command()
async def insult(ctx, member: discord.Member=None):
    if member:
        with open("insults.txt", "r") as f:
            read = f.read()
            array = read.split('\n')
            quote = random.choice(array)
            async with ctx.typing():
             await ctx.reply(f"{member.mention} {quote}")
    else:
        with open("insults.txt", "r") as f:
            read = f.read()
            array = read.split('\n')
            quote = random.choice(array)
            async with ctx.typing():
             await ctx.reply(f"{ctx.author.mention} {quote}")

#@bot.listen()
#async def on_message(message):
#    if '-vote' in message.content:
#        await ctx.send()
#@bot.command()
#@has_permissions(administrator=True)
#async def sudo(ctx, member: discord.Member, *, message=None):
#    await ctx.message.delete()
#    webhooks = await ctx.channel.webhooks()
#    for webhook in webhooks:
#        await webhook.delete()
#    webhook = await ctx.channel.create_webhook(name=member.name)
#    await webhook.send(str(message),
#                       username=member.name,
#                       avatar_url=member.avatar_url)


#with open("blacklist.json") as r:
#    word = json.load(r)
#
#
#def id(bot, message):
#    id = message.server.id
#    return word.get(id)



##########################ERROR HANDELING############################
@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**", colour=0x992d22)
        await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        embed = discord.Embed(title="<:cautionwarning:957442062838558761> An error has occurred!", description="**Expection: Not Found: 404**\n The command does not exist.", colour=0x992d22)
        #embed.set_footer(text=f"Use -help to get some useful commands!.", icon_url=f"{bot.user.avatar_url}")
        await ctx.send(embed=embed)
    # else:
    #    raise error


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="", description=f"There are {round(error.retry_after, 2)} Seconds left before you can try to use this Command again.", colour=0x992d22)
        await ctx.send(embed=embed)
    else:
        raise error


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="", description=f"<:cautionwarning:957442062838558761> That member was not found!", colour=0x992d22)
        embed.set_footer(text="If you think this was a mistake please report it per the bugreport command!")
        await ctx.send(embed=embed)
    #else:
    #    raise error


@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**", colour=0x992d22)
        await ctx.send(embed=embed)


#@admin.error
#async def admin_error(ctx, error):
#    if isinstance(error, commands.MissingPermissions):
#        embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**", colour=0x992d22)
#        await ctx.send(embed=embed)


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**", colour=0x992d22)
        await ctx.send(embed=embed)


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**", colour=0x992d22)
        await ctx.send(embed=embed)


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**", colour=0x992d22)
        await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**", colour=0x992d22)
        await ctx.send(embed=embed)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**", colour=0x992d22)
        await ctx.send(embed=embed)


@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="", description="**Hey! You Don\'t Have Permissions To Use That Command.**", colour=0x992d22)
        await ctx.send(embed=embed)

#####################################################LEVELING############################################

# remove the # to enable user leveling

# with open("users.json", "ab+") as ab:
##  ab.close()
# f = open('users.json','r+')
#   f.readline()
#   if os.stat("users.json").st_size == 0:
#  f.write("{}")
#  f.close()
# else:
#  pass
#
# with open('users.json', 'r') as f:
# users = json.load(f)
#
# @bot.event
# async def on_message(message):
#  if message.author.bot == False:
#   with open('users.json', 'r') as f:
# users = json.load(f)
# await add_experience(users, message.author)
# await level_up(users, message.author, message)
# with open('users.json', 'w') as f:
#  json.dump(users, f)
# await bot.process_commands(message)

# async def add_experience(users, user):
##  if not f'{user.id}' in users:
#        users[f'{user.id}'] = {}
#      users[f'{user.id}']['experience'] = 0
#      users[f'{user.id}']['level'] = 0
#  users[f'{user.id}']['experience'] += 6
# print(f"{users[f'{user.id}']['level']}")

# async def level_up(users, user, message):
#  experience = users[f'{user.id}']["experience"]
#  lvl_start = users[f'{user.id}']["level"]
# lvl_end = int(experience ** (1 / 4))
#  if lvl_start < lvl_end:
#   await message.channel.send(f':tada: {user.mention} has reached level {lvl_end}. Congrats! #:tada:', delete_after = 10)
# users[f'{user.id}']["level"] = lvl_end

# @bot.command()
# async def rank(ctx, member: discord.Member = None):
# if member == None:
#  userlvl = users[f'{ctx.author.id}']['level']
##   await ctx.send(f'{ctx.author.mention} You are at level {userlvl}!')
# else:
#  userlvl2 = users[f'{member.id}']['level']
# await ctx.send(f'{member.mention} is at level {userlvl2}!')

################################################################################################
#####################reaction roles#############################################################

##################################################################################################
# @tasks.loop(hours=24)
# async def myLoop():
#    await member.send("Hey! I would be proud if you upvote me!", delete_after=10)
#    await user.send("> `https://discordbotlist.com/bots/admin-helper/upvote`", delete_after=10)
# myLoop.start()
#######BUG REPORT NOTHING BELOW ALLOWED##############
from discord.ext.forms import Form

#possible_responses = ['Spamming this command will result in you being Blacklisted!', 'Being blacklisted will still show that it got sent but it didnt send it, so they have hope <:brish:952314587355684924>']


@slash.slash(name="help", description="Get help")
async def help(ctx: SlashContext):
    try:
        embeds = []
        embed = discord.Embed(title=f"Help Overview", colour=0x7289da)
        #embed.add_field(name=f"<:cautionwarning:957442062838558761> DOWNTIME <:cautionwarning:957442062838558761>", value=f"Expected Downtime!\nGet more Info's on [our Website!](https://www.admin-helper.tk/downtime.html)", inline=False)
        embed.add_field(name=f"Page 1", value=f"Help Overview", inline=False)
        embed.add_field(name=f"Page 2", value=f"All Non-Moderation commands", inline=False)
        embed.add_field(name=f"Page 3", value=f"Most Used Commands", inline=False)
        embed.add_field(name=f"Page 4", value=f"Fun Commands", inline=False)
        embed.add_field(name=f"Page 5", value=f"All Moderation Commands", inline=False)
        embed.add_field(name=f"Page 6", value=f"Whitelisted Commands", inline=False)
        embed.add_field(name=f"Page 7", value=f"Slash Commands", inline=False)
        embed.add_field(name=f"Page 8", value=f"Support", inline=False)
        embed.add_field(name=f"Invite Me Over", value=f"[Admin Helper](https://www.admin-helper.tk/)", inline=False)
        embed.set_footer(text="New website is planed!")
        embeds.append(embed)
        embed = discord.Embed(
            title="All commands:",
            description="", colour=0x7289da)
        embed.add_field(name="-insult [@user]",
                        value="Insult someone.",
                        inline=True)
        embed.add_field(name="-afk [reason] [time]",
                        value="Go afk for xy minutes.",
                        inline=True)
        embed.add_field(name="-invisping [@user] [text]",
                        value="Make an Invisible ping. Only PC user will see it!",
                        inline=True)
        embed.add_field(name="-gayquiz",
                        value="Take an gay quiz to prove your innocence ",
                        inline=True)
        embed.add_field(name="-8ball [question]",
                        value="Answers your question.",
                        inline=True)
        embed.add_field(name="-coinflip",
                        value="Flips a coin.",
                        inline=True)
        embed.add_field(name="-servercount",
                        value="See in how many Server Admin Helper is in.", inline=True)
        embed.add_field(name="-serverinfo",
                        value="Get informations about the server.", inline=True)
        embed.add_field(name="-whois [@user]",
                        value="Get informations about that user.", inline=True)
        embed.add_field(name="-membercount",
                        value="See how many member your server has.", inline=True)
        embed.add_field(name="-avatar [@user]",
                        value="Get the avatar of the user.", inline=True)
        embed.add_field(name="-meme",
                        value="See a random meme.", inline=True)
        embed.add_field(name="-gayrate [@user]",
                        value="See how gay the you or the Person is.", inline=True)
        embed.add_field(name="-pickup [@user]",
                        value="Get a pickup line.", inline=True)
        embed.add_field(name="-bugreport",
                        value="Fill out a form to send a bug-report", inline=True)
        embed.set_footer(text="Next page are Most used Commands")
        embeds.append(embed)
        embed = discord.Embed(
                        title="Most used Commands:",
                        description="", colour=0x7289da)
        embed.add_field(name="-gayrate [@user]", value="See how Gay you or another Person is.", inline=False)
        embed.add_field(name="-whois [@user]", value="Get informations about that user.", inline=False)
        embed.add_field(name="-servercount", value="See in how many Server Admin Helper is in.", inline=False)
        embed.set_footer(text="Next page are Fun Commands!")
        embeds.append(embed)
        embed = discord.Embed(
            title="Fun Commands:",
            description="", colour=0x7289da)
        embed.add_field(name="-meme", value="Get a random Meme.", inline=False)
        embed.add_field(name="-color [Hex]", value="See what color that HEX code is.", inline=False)
        embed.add_field(name="-translate [Language e.g de, fr, en] [Text]", value="Translate your text.", inline=False)
        embed.add_field(name="-morse [Text]", value="Make your text into Morse-code.", inline=False)
        embed.add_field(name="-wyr", value="Would you rather.", inline=False)
        embed.add_field(name="-chatbot [Text]", value="Chat with the bot.", inline=False)
        embed.add_field(name="-gayrate [@user]", value="See how Gay you or the Person is.", inline=False)
        embed.add_field(name="-joke", value="Get a random Joke.", inline=False)
        embed.add_field(name="-youtube [@user] [Text]", value="Publish a Fake YouTube comment.", inline=False)
        embed.set_footer(text="Next page are Moderation Commands!")
        embeds.append(embed)
        embed = discord.Embed(
            title="Moderation Commands:",
            description="", colour=0x7289da)
        embed.add_field(name="-ban [@user] [reason]", value="Ban the user.", inline=False)
        embed.add_field(name="-kick [@user] [reason]", value="Kick the user.", inline=False)
        embed.add_field(name="-slowmode [number]", value="Enable or Disable Slow mode.", inline=False)
        embed.add_field(name="-mute [@user] [reason]", value="Mute the user.", inline=False)
        embed.add_field(name="-unmute [@user] [reason]", value="Unmute the muted user.", inline=False)
        embed.add_field(name="-warn [@user] [reason]", value="Warn the user.", inline=False)
        embed.add_field(name="-prefix [prefix]", value="Make a new Prefix for the Server.", inline=False)
        embed.add_field(name="-poll [Question]", value="Make a poll for the Server.", inline=False)
        embed.add_field(name="-nick [@user] [nickname]", value="Nick the user.", inline=False)
        embed.add_field(name="-addpartner [invite link]", value="Want to find partners? Add your server.", inline=False)
        embed.add_field(name="-partners", value="Want to find a partner?", inline=False)
        embed.set_footer(text="Next page are Whitelisted Commands!")
        embeds.append(embed)
        embed = discord.Embed(
                        title="Whitelisted Commands:",
                        description="", colour=0x7289da)
        embed.add_field(name="-sudo [@user] [Text]", value="Send a message as the user.", inline=False)

        embed.set_footer(text="Next page is Support!")
        embeds.append(embed)
        embed = discord.Embed(
                        title="Slash Commands:",
                        description="", colour=0x7289da)
        embed.add_field(name="/chatbot [text]", value="Chat with the bot. Only you can see his responses.", inline=False)
        embed.add_field(name="/gayrate [@user]", value="See how gay you or the Person is.", inline=False)
        embed.add_field(name="/insult [@user]", value="Insult you or a Person.", inline=False)
        embed.add_field(name="/pickup [@user]", value="Get a pickup line.", inline=False)
        embed.add_field(name="/prefix [New Prefix]", value="Change the Prefix of the Server.", inline=False)
        embed.add_field(name="/statuses", value="See the status meanings of the bot.", inline=False)
        embed.set_footer(text="More questions/problems? Use -bugreport")
        embeds.append(embed)
        embed = discord.Embed(
                        title="Support:",
                        description="", colour=0x7289da)
        embed.add_field(name="Sudo Command Whitelisting", value="To get access to the Sudo command please use the -bugreport command.", inline=True)
        embed.add_field(name="Sudo Command Not Working?", value="The Sudo Command has a Maximum of 10 Uses in a Channel.\nThis can't be fixed due to Discord", inline=True)
        embed.add_field(name="-support", value="Get a Server invite to our Support Server.", inline=False)
        embed.add_field(name="-suggest", value="Suggest a command to Admin Helpers staff.", inline=False)
        embed.add_field(name="-credits", value="Credits/Contributors.", inline=False)
        embed.add_field(name="-partners", value="Admin Helper's partners.", inline=False)
        embed.add_field(name="-discovery", value="Admin Helper's Discovery status.", inline=False)
        #embed.add_field(name="-servercount", value="See in how many Server Admin Helper is in.")
        embed.set_footer(text="More questions/problems? Use -bugreport")
        embeds.append(embed)

        pages = 8
        cur_page = 1
        message1 = await ctx.send(f"Page {cur_page} of {pages}")
        message = await ctx.send(embed=embeds[cur_page-1])
        await message.add_reaction("◀")
        await message.add_reaction("▶")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀", "▶"]
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check=check)
                if str(reaction.emoji) == "▶" and cur_page < pages:
                    cur_page += 1
                    await message1.edit(content=f"Page {cur_page}/{pages}")
                    await message.edit(embed=embeds[cur_page-1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀" and cur_page > 1:
                    cur_page -= 1
                    await message1.edit(content=f"Page {cur_page} of {pages}")
                    await message.edit(embed=embeds[cur_page-1])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
            except:
                pass
            #except:
            #    await ctx.send("Something went wrong here!")
    except ctx.channel.type == discord.ChannelType.private:
        await ctx.send("Please use this command in a server")


@slash.slash(name="pickup", description="No females? 🧐")
async def pickup(ctx: SlashContext, member: discord.Member = None):
    if member:
        with open("pickup.txt", "r") as f:
            read = f.read()
            array = read.split('\n')
            quote = random.choice(array)
            await ctx.reply(f"{member.mention} {quote}")
    else:
        with open("pickup.txt", "r") as f:
            read = f.read()
            array = read.split('\n')
            quote = random.choice(array)
            await ctx.reply(f"{quote}", hidden=True)

@bot.command()
async def weather(ctx, *, country):
    async with aiohttp.ClientSession() as session:
        request = await session.get(f'https://api.popcat.xyz/weather?q={country}')
        weatherjson = await request.json()
        await ctx.send("About:**{}**\n\nCurrently: **{}**\n\nForecast: **{}**".format(weatherjson[0]["location"], weatherjson[0]["current"], weatherjson[0]["forecast"]))

@slash.slash(name="insult", description="Insult someone")
async def insult(ctx: SlashContext, member: discord.Member = None):
    member = member or ctx.author
    with open("insults.txt", "r", errors="ignore") as f:
        read = f.read()
        array = read.split('\n')
        quote = random.choice(array)
        await ctx.reply(f"{member.mention} {quote}")
    #else:
    #    with open("insults.txt", "r", errors="ignore") as f:
    #        read = f.read()
    #        array = read.split('\n')
    #        quote = random.choice(array)
    #        await ctx.reply(f"{ctx.author.mention} {quote}", hidden=True)

quoute = ['Lol...', 'Lmao...', 'HAHA...', 'Lmfao...']
@slash.slash(name="prefix", description="Change the bots prefix in this Server")
@has_permissions(administrator=True)
async def prefix(ctx: Context, new_prefix: str = None):
    #try:
        if ctx.guild is None:
            await ctx.reply("**You cannot change the prefix outside of a server silly!**")
            return

        if new_prefix is None:
            embed = discord.Embed(title="**Usage**", description=f"You can customize the Prefix using\n`-prefix [Your prefix]`!", colour=0x992d22)
            await ctx.send(embed=embed)
            return

        if len(new_prefix) > 20:
            await ctx.reply("**Prefix cannot be longer than 20 characters!**")
            return

        if new_prefix == '-':
            embed = discord.Embed(title="**I have set/reset the Prefix!**", description=f"`{new_prefix}`", colour=0x992d22)
            await ctx.guild.me.edit(nick=f"Admin Helper")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

            with open("prefixes.json", 'r') as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = new_prefix

            with open("prefixes.json", 'w') as f:
                json.dump(prefixes, f, indent=4)
        else:
            with open("prefixes.json", 'r') as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = new_prefix

            with open("prefixes.json", 'w') as f:
                json.dump(prefixes, f, indent=4)
                embed = discord.Embed(title="**Prefix changed to:**", description=f"`{new_prefix}`", colour=0x992d22)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=f"Also named myself to Admin Helper ({new_prefix})")
                await ctx.guild.me.edit(nick=f"Admin Helper ({new_prefix})")
                await ctx.send(embed=embed)
    #except Exception as e:
    #    embed = discord.Embed(title=random.choice(quoute), description=e, color=0x0000ff)
    #    await ctx.send(embed=embed)

@prefix.error
async def test(inter, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title=random.choice(quoute), description="You don't have permissions!", color=0x0000ff)
        await inter.send(embed=embed)

@slash.slash(name="Statuses", description="Bot Stautses")
async def statuses(ctx: SlashContext):
    embed = discord.Embed(title="Bot Status Meaning", description="", color=0x0000ff)
    embed.add_field(name="\u200b", value="<:online:962897421749342238> Means the bot has been restarted.", inline=False)
    embed.add_field(name="\u200b", value="<:dnd:962897421766119484> Means the bot is online.", inline=False)
    embed.add_field(name="\u200b", value="<:offline:962906229779361822> Means that the bot is currently offline.\nSeeing this should be reported to the Staff immediately!")
    await ctx.send(embed=embed, hidden=True)


@slash.slash(name="Chatbot", description="Chat with Admin Helper")
async def chatbot(ctx: SlashContext, *, text=None):
    async with aiohttp.ClientSession() as session:
        request = await session.get(f'https://api.popcat.xyz/chatbot?msg={text}&owner=Testical+Cutter&botname=Admin+Helper')
        jokejson = await request.json()
        await ctx.send(jokejson['response'], hidden=True)

@slash.slash(name="Weather", description="Get weather info and forecast on any place!")
async def weather(ctx: SlashContext, *, country):
    async with aiohttp.ClientSession() as session:
        request = await session.get(f'https://api.popcat.xyz/weather?q={country}')
        weatherjson = await request.json()
        await ctx.send("About:**{}**\n\nCurrently: **{}**\n\nForecast: **{}**".format(weatherjson[0]["location"], weatherjson[0]["current"], weatherjson[0]["forecast"]), hidden=True)
        #print(weatherjson)

@slash.slash(name="gayrate", description="Gayrate 💀")
async def gayrate(ctx: SlashContext, member: discord.Member = None):
    if ctx.author == 834530511790538763:
        embed = discord.Embed(title=f"", description=f'', colour=0x992d22)
        embed.add_field(name=f"Gayrate for my daddy:", value=f"{random.randint(0, 100)}%")
        await ctx.send(embed=embed)
    if member == None:
        embed = discord.Embed(title=f"", description=f'', colour=0x992d22)
        embed.add_field(name=f"Gayrate:", value=f"{random.randint(0, 100)}%")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"", description=f'', colour=0x992d22)
        embed.add_field(name=f"Gayrate:", value=f"{random.randint(0, 100)}%")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Request for {member.display_name}', icon_url=f"{member.avatar_url}")
        await ctx.send(embed=embed)

import aiohttp


@bot.command()
async def horny(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/horny?avatar={member.avatar_url_as(format="png")}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "horny.png")
            em = discord.Embed(
                title="bonk",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://horny.png")
            await ctx.send(embed=em, file=file)
         else:
             await ctx.send(error[0])
             await session.close()

@bot.command()
async def youtube(ctx, member: discord.Member = None, *, text):
    member = member or ctx.author
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/youtube-comment?avatar={member.avatar_url_as(format="png")}&username={member.display_name}&comment={text}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "twitter.png")
            em = discord.Embed(
                title="",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://twitter.png")
            await ctx.send(embed=em, file=file)
         else:
             await ctx.send(error[0])
             await session.close()


@bot.command()
async def discovery(ctx):
    #contents = ["Page 1/2!", "Page 2/2!"]
    pages = 2
    cur_page = 1
    message1 = await ctx.send(f"Page {cur_page}/{pages}")
    embed = discord.Embed(title="Admin Helpers Discovery Status:\nOnline. You can discover Admin Helper soon in Discord!\n", description="")
    embed.add_field(name="Verification and Safety <:3556orvoteyes:953351940975255592>", value="Your application must use slash commands, or have been approved for the Message Content privileged intent\n\nYour application must be verified\n\nYour Discord account must have Two-Factor authentication enabled\n\nYou must designate a community server as a support server for your application", inline=True)
    #embed.add_field(name="Your application must use slash commands, or have been approved for the Message Content privileged intent", value="\u200b", inline=True)
    #embed.add_field(name="Your application must be verified", value="\u200b", inline=True)
    #embed.add_field(name="Your Discord account must have Two-Factor authentication enabled", value="\u200b", inline=True)
    #embed.add_field(name="You must designate a community server as a support server for your application", value="\u200b", inline=True)
    embed.add_field(name="About Your Bot <:3556orvoteyes:953351940975255592>", value="Provide a short description for your application\n\nProvide a long description and tell us what your application does\n\nAdd at least one tag", inline=True)
    #embed.add_field(name="Provide a short description for your application", value="\u200b", inline=True)
    #embed.add_field(name="Provide a long description and tell us what your application does", value="\u200b", inline=True)
    #embed.add_field(name="Add at least one tag", value="\u200b", inline=True)
    embed.add_field(name="Application Links <:3556orvoteyes:953351940975255592>", value="Add an Install URL so people can add your application to their server\n\nProvide a link to your Terms of Service\n\nProvide a link to your Privacy Policy", inline=True)
    #embed.add_field(name="Add an Install URL so people can add your application to their server", value="\u200b", inline=True)
    #embed.add_field(name="Provide a link to your Terms of Service", value="\u200b", inline=True)
    #embed.add_field(name="Provide a link to your Privacy Policy", value="\u200b", inline=True)
    #embed.add_field(name="Your application's name may not contain any harmful or bad language", value="\u200b", inline=True)
    #embed.add_field(name="Your application's description may not contain any harmful or bad language", value="\u200b", inline=True)
    #embed.add_field(name="Your commands may not contain any harmful or bad language", value="\u200b", inline=True)
    message = await ctx.send(embed=embed)
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=120, check=check)
            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message1.edit(content=f"Page {cur_page}/{pages}")
                cur_page = 2
                embed = discord.Embed(title="Admin Helpers Discovery Status:\nOnline. You can discover Admin Helper soon in Discord!\n", description="")
                embed.add_field(name="Appropriate Language <:3556orvoteyes:953351940975255592>",
                                value="Your application's name may not contain any harmful or bad language\n\nYour application's description may not contain any harmful or bad language\n\nYour commands may not contain any harmful or bad language",
                                inline=False)
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message1.edit(content=f"Page {cur_page}/{pages}")
                cur_page = 1
                embed = discord.Embed(
                    title="Admin Helpers Discovery Status:\nOnline. You can discover Admin Helper soon in Discord!\n",
                    description="")
                embed.add_field(name="Verification and Safety <:3556orvoteyes:953351940975255592>",
                                value="Your application must use slash commands, or have been approved for the Message Content privileged intent\n\nYour application must be verified\n\nYour Discord account must have Two-Factor authentication enabled\n\nYou must designate a community server as a support server for your application",
                                inline=True)
                # embed.add_field(name="Your application must use slash commands, or have been approved for the Message Content privileged intent", value="\u200b", inline=True)
                # embed.add_field(name="Your application must be verified", value="\u200b", inline=True)
                # embed.add_field(name="Your Discord account must have Two-Factor authentication enabled", value="\u200b", inline=True)
                # embed.add_field(name="You must designate a community server as a support server for your application", value="\u200b", inline=True)
                embed.add_field(name="About Your Bot <:3556orvoteyes:953351940975255592>",
                                value="Provide a short description for your application\n\nProvide a long description and tell us what your application does\n\nAdd at least one tag",
                                inline=True)
                # embed.add_field(name="Provide a short description for your application", value="\u200b", inline=True)
                # embed.add_field(name="Provide a long description and tell us what your application does", value="\u200b", inline=True)
                # embed.add_field(name="Add at least one tag", value="\u200b", inline=True)
                embed.add_field(name="Application Links <:3556orvoteyes:953351940975255592>",
                                value="Add an Installation URL so people can add your application to their server\n\nProvide a link to your Terms of Service\n\nProvide a link to your Privacy Policy",
                                inline=True)
                # embed.add_field(name="Add an Installation URL so people can add your application to their server", value="\u200b", inline=True)
                # embed.add_field(name="Provide a link to your Terms of Service", value="\u200b", inline=True)
                # embed.add_field(name="Provide a link to your Privacy Policy", value="\u200b", inline=True)
                # embed.add_field(name="Your application's name may not contain any harmful or bad language", value="\u200b", inline=True)
                # embed.add_field(name="Your application's description may not contain any harmful or bad language", value="\u200b", inline=True)
                # embed.add_field(name="Your commands may not contain any harmful or bad language", value="\u200b", inline=True)
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()
            break


@bot.command()
async def gay(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format="png")}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "twitter.png")
            em = discord.Embed(
                title="",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://twitter.png")
            await ctx.send(embed=em, file=file)
         else:
             await ctx.send(error[0])
             await session.close()


@bot.command()
async def simpcard(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/simpcard?avatar={member.avatar_url_as(format="png")}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "twitter.png")
            em = discord.Embed(
                title="",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://twitter.png")
            await ctx.send(embed=em, file=file)
         else:
             await ctx.send(error[0])
             await session.close()

@bot.command()
async def transborder(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/transgender?avatar={member.avatar_url_as(format="png")}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "twitter.png")
            em = discord.Embed(
                title="",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://twitter.png")
            await ctx.send(embed=em, file=file)
         else:
             await ctx.send(error[0])
             await session.close()

#from datetime import datetime
#
#@bot.listen()
#async def on_member_join(member):
#    created = member.created_at
#    now = datetime.now()
#    delta = (now - created).days
#
#    if delta < 1:
#        await member.send(f'Hello there {member.mention}! I saw that your account is {delta} days old! Please wait till your account is 1 Days old!')
#        await member.kick()
#        #await message.channel.send('Detected alt account and kicked it!')

#@bot.command()
#@commands.is_owner()
#async def antialts(ctx, on=None, off=None):
#    try:
#        if on == "on":
#            bot.load_extension('antialts')
#            embed = discord.Embed(title="Anti-Alts activated!", description="")
#            await ctx.send(embed=embed)
#        if off == 'off':
#            embed = discord.Embed(title="Anti-Alts deactivated!", description="")
#            await ctx.send(embed=embed)
#            bot.unload_extension('antialts')
#    except commands.MissingPermissions:
#        embed = discord.Embed(title="Want to enable Anti-alts?", description=f"Use `-bugreport` And ask for it and send the server `ID`!")
#        embed.add_field(name="How to get the server ID?", value="Rightclick on the server and press \"Copy ID\"! Or use `-serverinfo`!")
#        await ctx.send(embed=embed)
#@bot.listen()
#@commands.is_owner()
#async def on_message(message):
#    if "-antialts off" in message.content:
#        bot.unload_extension('antialts')
#        embed = discord.Embed(title="Anti-Alts deactivated!", description="")
#        await message.channel.send(embed=embed)
#        bot.unload_extension('antialts')
#
#@bot.listen()
#@commands.is_owner()
#async def on_message(message):
#    if "-antialts on" in message.content:
#        bot.load_extension('antialts')
#        embed = discord.Embed(title="Anti-Alts activated!", description="")
#        await message.channel.send(embed=embed)

@bot.command()
async def pixelate(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format="png")}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "twitter.png")
            em = discord.Embed(
                title="",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://twitter.png")
            await ctx.send(embed=em, file=file)
         else:
             await ctx.send(error[0])
             await session.close()

@bot.command()
async def chatbot(ctx, *, text=None):
    try:
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.popcat.xyz/chatbot?msg={text}&owner=Testical+Cutter&botname=Admin+Helper')
            jokejson = await request.json()
            await ctx.send(jokejson['response'])
    except:
        await ctx.send(error[0])

@bot.command()
async def color(ctx, hex):
    try:
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.popcat.xyz/color/{hex}')
            jokejson = await request.json()
            #jokejson2 = await request.json()
            #jokejson3 = await request.json()
            embed = discord.Embed(title="", description="")
            embed.add_field(name="Hex", value=jokejson["hex"], inline=False)
            embed.add_field(name="Name", value=jokejson["name"], inline=False)
            embed.add_field(name="RGB", value=jokejson["rgb"], inline=False)
            embed.set_thumbnail(url=jokejson["color_image"])
            embed.add_field(name="Brightened", value=jokejson["brightened"], inline=False)
            await ctx.send(embed=embed)
    except:
        await ctx.send(error[0])

@bot.command(aliases = ["wyr"])
async def wouldyourather(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.popcat.xyz/wyr')
            jokejson = await request.json()
            jokejson2 = await request.json()
            embed = discord.Embed(title="", description="")
            embed.add_field(name="Would you rather", value=jokejson['ops1'], inline=False)
            embed.add_field(name="Or", value=jokejson2['ops2'], inline=False)
            await ctx.send(embed=embed)
    except:
        await ctx.send(error[0])

@bot.command()
async def joke(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/joke')
            jokejson = await request.json()
            await ctx.send(jokejson['joke'])
    except:
        await ctx.send(error[0])

@bot.command()
async def encode(ctx, text):
    try:
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.popcat.xyz/encode?text={text}')
            jokejson = await request.json()
            embed = discord.Embed(title="", description="")
            embed.add_field(name="Heres the encoded text", value=jokejson['binary'], inline=False)
            await ctx.send(embed=embed)
    except:
        await ctx.send(error[0])

    #I'm bi and love the color pink so much! I even think i'm transgender!! :D I want to be the Female in the relationship! And get it inside of me without condoms! I just hope its a big big big pp :)
@bot.command()
async def decode(ctx, text):
    try:
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.popcat.xyz/decode?binary={text}')
            jokejson = await request.json()
            embed = discord.Embed(title="", description="")
            embed.add_field(name="Heres the encoded text", value=jokejson['binary'], inline=False)
            await ctx.send(embed=embed)
    except:
        await ctx.send(error[0])

@bot.command()
async def morse(ctx, text):
    try:
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.popcat.xyz/texttomorse?text={text}')
            jokejson = await request.json()
            await ctx.send(jokejson['morse'])
    except:
        await ctx.send(error[0])


@bot.command(aliases = ["ss"])
async def screenshot(ctx, url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.popcat.xyz/screenshot?url={url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'screenshot.png'))
    except resp.status != 200:
        await ctx.send(error[0])

@bot.command()
async def translate(ctx, lang, *, text):
    try:
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.popcat.xyz/translate?to={lang}&text={text}')
            jokejson = await request.json()
            await ctx.send(jokejson['translated'])
    except:
        await ctx.send(error[0])

@bot.command(aliases = ["lgbtq", "lgbbq"])
async def lqbtqborder(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/lgbt?avatar={member.avatar_url_as(format="png")}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "twitter.png")
            em = discord.Embed(
                title="",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://twitter.png")
            await ctx.send(embed=em, file=file)
         else:
             await ctx.send(error[0])
             await session.close()

@bot.command()
async def upvotes(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discordbotlist.com/api/v1/bots/930842036360319067/widget") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'screenshot.png'))
    except resp.status != 200:
        await ctx.send(error[0])


@bot.command(pass_context=True)
async def afk(ctx, reason=None, minutes=60):
    current_nick = ctx.author.nick
    await ctx.send(f"{ctx.author.mention} I set your AFK to {reason} for {minutes} minutes")
    await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")

    counter = 0
    while counter <= minutes:
        counter += 1
        await asyncio.sleep(60)
        if counter == minutes:
            await ctx.author.edit(nick=current_nick)
            await ctx.send(f"{ctx.author.mention}, your AFK time has expired!")
            break


@bot.command(aliases = ["lm"])
async def lovemeter(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.popcat.xyz/ship?user1={ctx.author.avatar_url}&user2={member.avatar_url}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "ship.png")
            em = discord.Embed(
                title="",
                description=f"Love meter or {ctx.author.mention} and {member.mention}!\n{random.randint(0, 100)}%",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://ship.png")
            await ctx.send(embed=em, file=file)
         else:
             await ctx.send(error[0])
             await session.close()

@bot.command()
async def drake(ctx, text, text2):
    try:
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.popcat.xyz/drake?text1={text}&text2={text2}') as af:
             if 300 > af.status >= 200:
                fp = io.BytesIO(await af.read())
                file = discord.File(fp, "drake.png")
                em = discord.Embed(
                    title="",
                    color=0xf1f1f1,
                )
                em.set_image(url="attachment://drake.png")
                await ctx.send(embed=em, file=file)
             else:
                await ctx.send(error[0])
                await session.close()
    except Exception as e:
        print(e)

@bot.command()
async def alert(ctx, *, text):
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.popcat.xyz/alert?text={text}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "twitter.png")
            em = discord.Embed(
                title="",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://twitter.png")
            await ctx.send(embed=em, file=file)
         else:
            await ctx.send(error[0])
            await session.close()

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def bugreport(ctx):
    blacklist = []
    embed = discord.Embed(title="Please keep in mind that;", description="**We store your User ID for __at least__ one month!\nEvery answer is being Logged!\n\nYou can always type __`stop`__ to cancel this report!**", colour=0x992d22)
    await ctx.send(embed=embed)
    form = Form(ctx,'Bug Report')
    form.add_question('What happened?','first')
    form.add_question('What should happen?','second')
    form.add_question('How to reproduce?','third')
    form.add_question('Additional Message', 'add')
    #form.add_cancelkeyword('stop')
    #form.add_question('Additional Message:', 'add')
    form.edit_and_delete(True)
    await form.set_color("#992d22")
    result = await form.start()
    async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dogjson = await request.json()
    embed = discord.Embed(title="", description="**This has been delivered to the Developer Team of Admin Helper!**", colour=0x992d22)
    embed.add_field(name='While our Team is getting ready to answer you.\n\nEnjoy the picture!', value=f"\u200b", inline=False)
    embed.set_image(url=dogjson['link'])
    embed.set_footer(text="If you used stop this will be delivered!")
    await ctx.send(embed=embed)
    #embed = discord.Embed(title=roblox"", description=f"{random.choice(possible_responses)}")
    #await ctx.send(embed=embed)
    auser = bot.get_user(int(834530511790538763))
    embed = discord.Embed(title="New Bugreport!", description="Username: **{}**\nID:**{}**\n\nBug Report Answers:\n\nWhat happened?: **{}**\nWhat should happen?: **{}**\nHow to reprodouce?: **{}**\nAdditional Message: **{}**".format(ctx.author, ctx.author.id, result.first, result.second, result.third, result.add))
    await auser.send(embed=embed)
    return result


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def gayquiz(ctx):
    variable = 0
    form = Form(ctx,'Gay quiz')
    form.add_question('Are you attracted to men?','first')
    form.add_question('Do you like big pp\'s in your 🍑?','second')
    form.add_question('Do you get hard when u see men?','third')
    form.add_question('Did you ever look at a man and think "Oh god hes hot"?','fourth')
    form.add_question('Did you ever have a girlfriend?','fifth')
    form.add_question('Are you french?', 'add')
    form.edit_and_delete(True)
    await form.set_color("#992d22")
    result = await form.start()
    if result.first.lower() == "yes":
        variable += 1
    if result.second.lower() == "yes":
        variable += 1
    if result.third.lower() == "yes":
        variable += 1
    if result.add.lower() == "yes":
        variable += 1
    if result.fourth.lower() == "yes":
        variable += 1
    if result.fifth.lower() == "no":
        variable += 1

    #if variable > 3:
    #    embed = discord.Embed(title="Your results!", description=f"{variable}/4! So you're gay!")
    #    await ctx.send(embed=embed)
#
    #if variable < 4:
    #    embed = discord.Embed(title="Your results!", description=f"{variable}/4! So you're not gay! Chad")
    #    await ctx.send(embed=embed)
    if variable < 4:
        embed = discord.Embed(title="Your results!", description=f"{variable}/4! You aren't gay!")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Your results!", description=f"{variable}/4! You're gay!")
        await ctx.send(embed=embed)
    return result

#@bot.command()
#async def partners(ctx):
#    try:
#        #guild1 = await bot.fetch_guild(950135047439138816)
#        guild = bot.get_guild(971465291404029993)
#        embed = discord.Embed(title="Admin Helper's partners", description="")
#        embed.add_field(name="SD Protect", value=f"350 Members! [Join](https://discord.gg/QujeWGHhb9)", inline=False)
#        embed.add_field(name="ShitPost LORE", value=f"{str(guild.member_count)} Members! [Join](https://discord.gg/ATTgm7FXPf)", inline=False)
#        await ctx.send(embed=embed)
#    except Exception as e:
#        await ctx.send(e)

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def suggest(ctx):
    blacklist = []
    embed = discord.Embed(title="Please keep in mind that;", description="**We store your User ID for __at least__ one month!\nEvery suggestion is being Logged!\n\nYou can always type __`stop`__ to cancel this suggestion!**", colour=0x992d22, delete_after=10)
    await ctx.send(embed=embed)
    form = Form(ctx,'Suggestion')
    form.add_question('Whats the name of the command?','first')
    form.add_question('What should happen if you use it?','second')
    form.add_question('Slash command or Prefix command?','third')
    form.add_question('Additional Request', 'add')
    form.add_question('Questions?', 'add2')
    #form.add_cancelkeyword('stop')
    #form.add_question('Additional Message:', 'add')
    form.edit_and_delete(True)
    await form.set_color("#992d22")
    result = await form.start()
    async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dogjson = await request.json()
    embed = discord.Embed(title="", description="**This has been delivered to the Developer Team of Admin Helper!**", colour=0x992d22)
    embed.add_field(name='While our Team is getting ready to review this request.\n\nEnjoy the picture!', value=f"\u200b", inline=False)
    embed.set_image(url=dogjson['link'])
    #embed.add
    embed.set_footer(text="If you used stop this will be delivered!")
    await ctx.send(embed=embed, delete_after=25)
    #embed = discord.Embed(title=roblox"", description=f"{random.choice(possible_responses)}")
    #await ctx.send(embed=embed)
    auser = bot.get_channel(int(971152651674869770))
    embed = discord.Embed(title="New Suggestion!", description="Username: **{}**\nID:**{}**\n\nSuggestion:\n\nWhats the name of the command?: **{}**\nWhat should happen if you use it?: **{}**\nSlash command or Prefix command?: **{}**\nAdditional Request: **{}**\nQuestions: **{}**".format(ctx.author, ctx.author.id, result.first, result.second, result.third, result.add, result.add2))
    await auser.send(embed=embed)
    return result


#@bot.command()
#@commands.is_owner()
#async def reply(ctx, *, text, member: discord.Member):
#    with open('bugreport.txt', 'r') as file:
#        ids = tuple((int(x.strip()) for x in file.readlines() if x.strip().isdecimal()))
#        if ctx.message.author in ids:
#            embed = discord.Embed(title="", description=f"<:GreenTick:957279366499409950> ***Owner*** {ctx.author.name} has replied!\n{text}!", colour=0x2ecc71)
#            embed.set_footer(text="Copyright (©) 2022 Admin Helper Team", icon_url=f"{ctx.author.avatar_url}")
#            await member.send(embed=embed)
#        else:
#            await ctx.send(error[0])

@bot.listen()
async def on_message(message):
    if 'https://grabify.link/' in message.content:
        await message.delete()
        em = discord.Embed(title=f"", description=f"**<:cautionwarning:957442062838558761> Whoa there! {message.author.mention} This is a dangerous link!**", color=0x992d22)
        await message.channel.send(embed=em)


@bot.listen()
async def on_message(message):
    if 'https://who-tf.ru/asked/' in message.content:
        await message.delete()
        em = discord.Embed(title=f"", description=f"**<:cautionwarning:957442062838558761> Whoa there! {message.author.mention} This is a weird looking link!**", color=0x992d22)
        await message.channel.send(embed=em)

uptime.start()
bot.run("OTMwODQyMDM2MzYwMzE5MDY3.Yd7wMw.6PHqPeY8H-xSpg_Oi3IHKuo5pYY")
