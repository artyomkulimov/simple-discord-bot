import json
import discord
from random import randint
from discord.ext import commands

with open("my own bot\database\puns.json", "r") as file:
    puns = json.load(file)
for punishment in puns["pun-times"]:
    if punishment["time"] == 0 and punishment["type"] == "mute":
        unmuted = punishment["uid"]
        puns["pun-times"].remove(punishment)
    if punishment["time"] == 0 and punishment["type"] == "ban":
        unbanned = punishment["uid"]
        puns["pun-times"].remove(punishment)

class Refresh(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def refreshmutes(self, ctx):
        member = await ctx.guild.fetch_member(int(unmuted))
        mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
        await member.remove_roles(mutedRole)
        embed = discord.Embed(
            description=f"✅ **{member.display_name}#{member.discriminator} has been unmuted**",
            ccolor=0xFFFF55,
        )
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def refreshbans(self, ctx):
        user = await client.fetch_user(unbanned)
        await ctx.guild.unban(user)
        embed = discord.Embed(
            description=f"✅ **The user {unbanned} has been unbanned**",
            ccolor=0xFFFF55,
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Refresh(bot))