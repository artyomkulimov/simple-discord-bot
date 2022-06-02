import discord  # Imports the discord module.
from discord.ext import commands  # Imports discord extensions.
from discord.utils import get
import json

# Loads .json file
# with open("my own bot\database\puns.json", "r") as file:
#     puns = json.load(file)
# searches for players who should be unbanned
# #Saves data to .json file
print("hi1")
# The below code verifies the "client".
client = commands.Bot(command_prefix=".")
# The below code stores the token.
token = (
    "BOT TOKEN HERE"
)
print("hi2")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all requirements.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "You do not have the required permissions to complete this command."
        )

print("hi3")
@client.command()
@commands.has_permissions(administrator=True)
async def announce(ctx):
    channel = client.get_channel(971438740524372018)
    em = discord.Embed(
        title="__Information__",
        description="""
        **What is Speedwell?**
        Speedwell is a custom cave-mining server with Boss Battles, PvP, Custom Items, and more! 

        **When is it coming out?**
        Release should be in a few weeks. Staff applications are open right now! If you'd like to help speed up the process, go [__apply__](http://corn-hub.blogspot.com/)!

        **How can I support the server in its development?**
        You can support the server by purchasing a rank [__here__](http://corn-hub.blogspot.com/).
        You can also support by just inviting your friends to the discord, or boosting!
        """,
        color=0xFFFF55,
        # timestamp=datetime.datetime.utcnow(),
    )
    em.set_footer(
        text=f"If you have any other questions, please reach out using our ticket system."
    )
    await channel.send(embed=em)

print("hi4")
client.run(token)
