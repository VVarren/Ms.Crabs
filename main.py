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
from discord.ext import tasks

#Start Client
client = discord.Client()

#Open/Close the NotSusFile 
file = open("DONOTLOOKHERE.txt","r")
words = file.read().splitlines()
file.close()

#Var
BrowniePoints = defaultdict(lambda:3)
Thanks = set()

#The meats of the file. IDk how to title this lol.
@client.event
async def on_ready():
    print('Ms.Crabs has been fired up by {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client:
        return
    #loop over the message and search for bad words
    for word in words:
        if word in message.content.lower():
            await message.channel.send('You have offended the law, now FACE JUDGEMENT!! -1bp(Bronwie Points)')
            BrowniePoints[message.author] -= 1
            print(BrowniePoints)
            if BrowniePoints[message.author] == 2:
                await message.channel.send('You have 2 more bp. Please avoid cussing, you will be kicked when you reach 0')
            if BrowniePoints[message.author] == 1:
                await message.channel.send('This is your last chance before being kicked')
            #Kick them off the server if they have 0 bp
            if BrowniePoints[message.author] == 0:
                await message.guild.kick(message.author,reason = 'bp was too low')
    #The thank system
    if message.content.lower().startswith("thank"):
        if message.author in Thanks:
            await message.channel.send('Please wait 24 after your initial thank to thank again.')
            return
        Thanks.add(message.author)
        for mention in message.mentions:
            BrowniePoints[mention] += 1
        
            if BrowniePoints[mention] > 3:
                BrowniePoints[mention] = 3
            await message.channel.send(f'You have thanked {mention}. They now have {BrowniePoints[mention]} bp')
    if message.content.startswith("$bp"):
        bpamount = discord.Embed(description = f'You have {BrowniePoints[message.author]} bp')
        await message.channel.send(embed = bpamount)
    if message.content.startswith("$help"):
        assistance = discord.Embed(description = 'To thank someone you type \'thank @user \'\nTo check your brownie points(bp), \'use $bp\'\n(Do not include the quotes)')
        await message.channel.send(embed = assistance)
#Need to do help



#reset the thank
@tasks.loop(hours = 24)
async def thank():
    global Thanks
    Thanks = set()

thank.start()
client.run(os.getenv('TOKEN'))
