#Python Bot that I have coded

import os
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('Ms.Crabs is fired up by {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.getenv('TOKEN'))
