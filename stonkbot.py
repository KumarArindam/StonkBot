import os
import discord
from discord import channel
from dotenv import load_dotenv
from stock_data import *
from constant import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    author = message.author
    if author == client.user:
        return

    messageContent = message.content.lower()
    messageContent = messageContent.strip()
    if messageContent.startswith('!hello'):
        print('on_message !test')
        await test(author, message)

    if messageContent.startswith('!track'):
        print('on_message !track')
        await track_intitate(author, message, messageContent)


async def track_intitate(author, message, messageContent):
    print("in track_initiated function")
    await message.channel.send('Tracking initiated for {} at {} levels'.format( \
                                messageContent.split()[-2], messageContent.split()[-1]))
    await message.author.send('Tracking initiated for {} at {} levels'.format( \
                                messageContent.split()[-2], messageContent.split()[-1]))

async def test(author, message):
    print('in test function')
    await message.channel.send('Fuck you {}'.format(author))        
    

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        "Well well if this ain't the prodigal son {}. Welcome motherfucker!".format(member.name)
    )


@client.event
async def on_ready():
    print("Logged in as {}".format(client.user.name))
    print('Client Id:- {} \n'.format(client.user.id))
    
    for guild in client.guilds:
        if guild.name == GUILD:
            break

        print('{} has connected to Discord!'.format(client.user))
        print('server name = {} and server ID = {}'.format(guild.name, guild.id))

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

    channel = client.get_channel(WATCHLIST_CHANNEL_ID)
    await channel.send("Beta Testing. Please do not reply!")
    # stock_data = get_closing_data(stock_list)
    # await channel.send(stock_data)

client.run(TOKEN)

