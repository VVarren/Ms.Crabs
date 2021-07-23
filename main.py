'''
Functions I want:
Find a way to track each person and their status on how many times they have cussed
Profanity filter. 3 times and you out. Warning each Time.

Loop over the txt and see if any of the words are in the message
if word is in message, give warning

'''
#FOR FUTURE WARREN: LOOK AT MEMBER CACHE AT https://discordpy.readthedocs.io/en/latest/intents.html

#Imports
import os
import discord
from collections import defaultdict

#Start Client
client = discord.Client()

#Open/Close the NotSusFile 
file = open("DONOTLOOKHERE.txt","r")
words = file.read().splitlines()
file.close()

#Var
BrowniePoints = defaultdict(lambda:3)


#The meats of the file. IDk how to title this lol.
@client.event
async def on_ready():
    print('Ms.Crabs has been fired up by {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client:
        return
    for word in words:
        if word in message.content.lower():
            await message.channel.send('You have offended the law, now FACE JUDGEMENT!! -1bp(Bronwie Points)')
            BrowniePoints[message.author] -= 1
            print(BrowniePoints)
            if BrowniePoints[message.author] == 0:
                await message.guild.kick(message.author,reason = 'bp was too low')
    if message.content.lower().startswith("thank"):
        for mention in message.mentions:
            BrowniePoints[mention] += 1
            if BrowniePoints[mention] > 3:
                BrowniePoints[mention] = 3
            await message.channel.send(f'You have thanked {mention}. They now have {BrowniePoints[mention]} bp')



#@tasks.loop(seconds = 5)
#async def giver():
#   pass

client.run(os.getenv('TOKEN'))
