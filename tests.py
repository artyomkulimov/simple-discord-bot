import interactions
from interactions import Button, ButtonStyle, Channel
import random
import pprint
import json
import siaskynet as skynet
import datetime  # Imports datetime

bot = interactions.Client(
    "BOT TOKEN HERE"
)
gid = 971121874048258119
pp = pprint.PrettyPrinter(indent=4)
logs = []
client = skynet.SkynetClient()


@bot.event
async def on_ready():
    print("Ready!")


@bot.command(
    name="cticket",
    description="A simple example",
    scope=gid,
)
async def create_ticket(ctx: interactions.CommandContext):
    em = interactions.Embed(
        title="Request Support",
        description="""
        Click the button below to get in touch with our staff team about any problems you are experiencing.
        """,
        color=0xFFFF55,
        # timestamp=datetime.datetime.utcnow(),
    )
    # em.set_footer(text=f"powered by")
    button = Button(
        style=ButtonStyle.PRIMARY,
        emoji=interactions.Emoji(name="📩"),
        label="Create Ticket!",
        custom_id="createticket",
    )
    await ctx.send(embeds=em, components=button)


@bot.component("createticket")
async def create_channel(ctx: interactions.ComponentContext):
    global ticketnum
    global creator
    global timecreated
    x = datetime.datetime.now()
    timecreated = x.strftime("%A, %B %d, at %X")
    creator = ctx.author.mention
    await ctx.get_guild()
    with open("my own bot\database\\tickets.json", "r") as file:
        ticketnum = json.load(file)
    ticketnum += 1
    with open("my own bot\database\\tickets.json", "w") as file:
        json.dump(ticketnum, file)
    channel = await ctx.guild.create_channel(
        f"ticket-{ticketnum}", type=interactions.ChannelType.GUILD_TEXT
    )

    # print(ticketnum)
    createdticket = interactions.Embed(
        title="Ticket",
        description=f"""
        Opened a new ticket: {channel.mention}
        """,
        color=0xFFFF55,
        # timestamp=datetime.datetime.utcnow(),
    )
    await ctx.send(embeds=createdticket, ephemeral=True)
    # create embed for when the ticket is opened
    generalTicket = interactions.Embed(
        title=f"General Ticket Number {ticketnum}",
        description=f"""
        Thank you for making a ticket.
        Please describe your issue in detail {ctx.author.mention}
        """,
        color=0xFFFF55,
        # timestamp=datetime.datetime.utcnow(),
    )
    # create button for when ticket is opened
    closeButton = Button(
        style=ButtonStyle.DANGER,
        # emoji=interactions.Emoji(name="📩"),
        label="Close",
        emoji=interactions.Emoji(name="🔒"),
        custom_id="deleteticket",
    )
    await channel.send(embeds=generalTicket, components=closeButton)


@bot.component("deleteticket")
async def delete_channel(ctx: interactions.ComponentContext):
    global destroyer
    global timedestroyed
    x = datetime.datetime.now()
    timedestroyed = x.strftime("%A, %B %d, at %X")
    creator = ctx.author.mention
    destroyer = ctx.author.mention
    channel = Channel(
        **await bot._http.get_channel(ctx.channel_id), _client=bot._http
    )
    messages = await bot._http.get_channel_messages(ctx.channel_id)
    for message in messages:
        with open(
            f"my own bot\database\\reversed\{ticketnum}.txt", "a+"
        ) as file_object:
            # Append text at the end of file
            if message["attachments"]:
                file_object.write(
                    f'{message["author"]["username"]}:  {message["content"]} URL={message["attachments"][0]["url"]}\n'
                )
            if message["embeds"]:
                file_object.write(
                f'{message["author"]["username"]}:  {message["embeds"][0]["description"]}\n{message["embeds"][0]["title"]}\nembed:\n'
            )
            file_object.write(
                f'{message["author"]["username"]}:  {message["content"]}\n'
            )
            # logs.append(
            #     f'{message["author"]["username"]}:  {message["content"]}'
            # )
    with open(f'my own bot\database\\reversed\{ticketnum}.txt') as f,  open(f'my own bot\database\\ticket-logs\{ticketnum}.txt', 'w') as file:
        file.writelines(reversed(f.readlines()))
    # print(logs)
    await channel.delete()
    link = client.upload_file(
        f"my own bot\database\\ticket-logs\{ticketnum}.txt"
    )
    link = str(link).lstrip("sia://")
    # print(link)
    channel = Channel(
        **await bot._http.get_channel(972092713468063764), _client=bot._http
    )
    # create archive embed
    ticketArchive = interactions.Embed(
        title="Ticket Closed",
        color=0xFFFF55,
        # timestamp=datetime.datetime.utcnow(),
    )
    ticketArchive.add_field(
        name="Ticket ID", value=f"{ticketnum}", inline=True
    )
    ticketArchive.add_field(name="Opened By", value=f"{creator}", inline=True)
    ticketArchive.add_field(
        name="Closed By", value=f"{destroyer}", inline=True
    )
    ticketArchive.add_field(name="Reason closed", value="<none>", inline=False)
    ticketArchive.add_field(
        name="Archive",
        value=f"[Click Here!](https://fileportal.org/{link})",
        inline=True,
    )
    ticketArchive.add_field(
        name="Open Since", value=f"{timecreated}", inline=True
    )
    ticketArchive.add_field(
        name="Closed at", value=f"{timedestroyed}", inline=True
    )
    # ticketArchive.add_field(
    #     name="Field 8 Title", value="It is inline with Field 6", inline=True
    # )
    # ticketArchive.add_field(
    #     name="Field 9 Title", value="It is inline with Field 6", inline=True
    # )
    await channel.send(embeds=ticketArchive)
    # print(ctx.author)
    # print(ctx.author.user)
    # print(ctx.author)


bot.start()
