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
    messageContent = message.content.lower()
    messageContent = messageContent.strip()
    print(messageContent)
    
    if author == client.user:
        return
    elif(messageContent.startswith('!')):
        cmd = message.content.split()[0].replace("_","")

        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]

        ## Bot commands

        if(cmd == 'hello' or cmd =='hi'):
            await welcome_message(author, message)
        elif(cmd =='track'):
            print('executing track_stock')
            await track_stock(author, message, messageContent)


async def track_stock(author, message, messageContent):
    print("in track_initiated function")
    await message.channel.send('Tracking initiated for {} at {} levels'.format( \
                                messageContent.split()[-2], messageContent.split()[-1]))
    await message.author.send('Tracking initiated for {} at {} levels'.format( \
                                messageContent.split()[-2], messageContent.split()[-1]))

async def welcome_message(author, message):
    print('in welcome_message function')
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
        print('{} has connected to Discord!'.format(client.user))
        print('server name = {} and server ID = {}'.format(guild.name, guild.id))
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
        if guild.name == GUILD:
            break

    channel = client.get_channel(WATCHLIST_CHANNEL_ID)
    await channel.send("Beta Testing. Please do not reply!")
    stock_data = get_closing_data(stock_list)
    await channel.send(stock_data)

client.run(TOKEN)

