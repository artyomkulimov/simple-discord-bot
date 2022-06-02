import discord  # Imports the discord module.
from discord.ext import commands  # Imports discord extensions.
from discord.utils import get
import random  # Imports random
import datetime  # Imports datetime
import asyncio
import json

# Loads .json file
with open("my own bot\database\puns.json", "r") as file:
    puns = json.load(file)
# searches for players who should be unbanned
# #Saves data to .json file

# The below code verifies the "client".
client = commands.Bot(command_prefix="!")
# The below code stores the token.
token = (
    "BOT TOKEN HERE"
)

for punishment in puns["pun-times"]:
    if punishment["time"] == 0 and punishment["type"] == "mute":
        unmuted = punishment["uid"]
        puns["pun-times"].remove(punishment)
    if punishment["time"] == 0 and punishment["type"] == "ban":
        unbanned = punishment["uid"]
        puns["pun-times"].remove(punishment)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all requirements.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "You do not have the required permissions to complete this command."
        )


@client.command()
@commands.has_permissions(administrator=True)
async def refreshmutes(ctx):
    member = await ctx.guild.fetch_member(int(unmuted))
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(mutedRole)
    embed = discord.Embed(
        description=f"✅ **{member.display_name}#{member.discriminator} has been unmuted**",
        ccolor=0xFFFF55,
    )
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def refreshbans(ctx):
    user = await client.fetch_user(unbanned)
    await ctx.guild.unban(user)
    embed = discord.Embed(
        description=f"✅ **The user {unbanned} has been unbanned**",
        ccolor=0xFFFF55,
    )
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, msg, title):
    channel = client.get_channel(971438740524372018)
    em = discord.Embed(
        title=title,
        description=msg,
        color=0xFFFF55,
        # timestamp=datetime.datetime.utcnow(),
    )
    x = datetime.datetime.now()
    em.set_footer(
        text=f"If you have any other questions, please reach out using our ticket system."
    )
    await channel.send(embed=em)


# The below code bans player.
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, time, reason=None):
    await member.ban(reason=reason)
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    tempban = int(time[0]) * time_convert[time[-1]]
    # case number, logging time
    with open("my own bot\cases.json", "r") as file:
        casenum = json.load(file)
    casenum += 1
    with open("my own bot\cases.json", "w") as file:
        json.dump(casenum, file)
    # done with case numbers, time for punishements
    with open("my own bot\puns.json", "r") as file:
        bans = json.load(file)
    bans["pun-times"].append(
        {"casenum": casenum, "uid": member.id, "time": tempban, "type": "ban"}
    )
    with open("my own bot\puns.json", "w") as file:
        json.dump(bans, file)
    # done with bans
    channel = client.get_channel(971141286373503087)
    em = discord.Embed(
        title=f"Ban | Case {casenum}",
        description=f"""
        **Responsible Moderator**: {ctx.author}
        **Offender**: {member}
        **Duration**: {time}
        **Reason**: {reason}

        """,
        color=0xFFFF55,
    )
    x = datetime.datetime.now()
    em.set_footer(text=f"{x.strftime('%A, %B %d, at %X')}")
    await channel.send(embed=em)
    channel = await member.create_dm()
    await channel.send(embed=em)
    await member.ban()
    await asyncio.sleep(tempban)
    await member.unban()


# The below code unbans player.
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (
            member_name,
            member_discriminator,
        ):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


# The below code kicks the member
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    # send the logs
    channel = client.get_channel(971141286373503087)
    em = discord.Embed(
        title=f"Kick | Case {random.randint(7355,49423)}",
        description=f"""
        **Responsible Moderator**: {ctx.author}
        **Offender**: {member}
        **Reason**: {reason}

        """,
        color=0xFFFF55,
        # timestamp=datetime.datetime.utcnow(),
    )
    x = datetime.datetime.now()
    em.set_footer(text=f"{x.strftime('%A, %B %d, at %X')}")
    await channel.send(embed=em)
    channel = await member.create_dm()
    await channel.send(embed=em)


# Mute command
@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, time, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="muted")
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    tempmute = int(time[0]) * time_convert[time[-1]]

    await member.add_roles(muted_role)
    # logger
    with open("my own bot\cases.json", "r") as file:
        casenum = json.load(file)
    casenum += 1
    with open("my own bot\cases.json", "w") as file:
        json.dump(casenum, file)
    # casenum
    channel = client.get_channel(971141286373503087)
    em = discord.Embed(
        title=f"Mute | Case {casenum}",
        description=f"""
        **Responsible Moderator**: {ctx.author}
        **Offender**: {member}
        **Duration**: {time}
        **Reason**: {reason}

        """,
        color=0xFFFF55,
    )
    x = datetime.datetime.now()
    em.set_footer(text=f"{x.strftime('%A, %B %d, at %X')}")
    await channel.send(embed=em)
    channel = await member.create_dm()
    await channel.send(embed=em)
    with open("my own bot\puns.json", "r") as file:
        bans = json.load(file)
    bans["pun-times"].append(
        {
            "casenum": casenum,
            "uid": member.id,
            "time": tempmute,
            "type": "mute",
        }
    )
    with open("my own bot\puns.json", "w") as file:
        json.dump(bans, file)
    await asyncio.sleep(tempmute)
    await member.remove_roles(muted_role)


# unmute command
@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
    # finish loading the case number for later assignment
    await member.remove_roles(mutedRole)
    embed = discord.Embed(
        description=f"✅ **{member.display_name}#{member.discriminator} unmuted successfuly**",
        ccolor=0xFFFF55,
    )
    await ctx.send(embed=embed, delete_after=5)

    channel = client.get_channel(971141286373503087)

    em = discord.Embed(
        title=f"Unmute | Case unmute, no case number",
        description=f"""
        **Responsible Moderator**: {ctx.author}
        **Offender**: {member}
        """,
        color=0xFFFF55,
    )

    x = datetime.datetime.now()
    em.set_footer(text=f"{x.strftime('%A, %B %d, at %X')}")
    await channel.send(embed=em)
    channel = await member.create_dm()
    await channel.send(embed=em)


client.run(token)
