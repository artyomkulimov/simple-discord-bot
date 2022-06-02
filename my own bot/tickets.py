import discord
from discord.ext import commands
from discord.utils import get
from discord_components import (
    DiscordComponents,
    ComponentsBot,
    Button,
    SelectOption,
    Select,
)
import random

client = commands.Bot(command_prefix="!")
token = (
    "BOT TOKEN HERE"
)
DiscordComponents(client)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all requirements.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "You do not have the required permissions to complete this command."
        )
    await ctx.send(error)


@client.command()
async def ticket(ctx):
    em = discord.Embed(
        title="Request Support",
        description="""
        Click the button below to get in touch with our staff team about any problems you are experiencing.
        """,
        color=0xFFFF55,
        # timestamp=datetime.datetime.utcnow(),
    )
    em.set_footer(text=f"powered by")
    compo = Button(
        label="Create Ticket!", style="3", emoji="📩", custom_id="button1"
    )
    await ctx.send(embed=em, components=[compo])
    interaction = await client.wait_for(
        "button_click", check=lambda i: i.custom_id == "button1"
    )
    await interaction.send(content="opening a new channel!", ephemeral=False)
    await ctx.get_guild()
    channel = await ctx.guild.create_channel(random.randint(192, 1920))


client.run(token)
