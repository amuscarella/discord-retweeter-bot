#######################################################################
# 
#######################################################################

import discord

#read token
TOKEN = open("token.txt", 'r').readline()

#declare discord intents & initialize client
intents = discord.Intents.default()
intents.mesages = True
intents.members = True
intents.guilds = True

Client = discord.Client(intents = intents)