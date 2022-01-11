#######################################################################
# Discord Retweeter
# Authors: Antonio Muscarella (Github: amuscarella)
#######################################################################
import discord
#Local imports
from config import *
#######################################################################
# Intents Declaration & Client Initialization
#######################################################################
#read token
TOKEN = open(TOKEN_FNAME, 'r').readline()

#declare discord intents & initialize client
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents = intents)
#######################################################################
# App Functions
#######################################################################
@client.event
async def on_ready():
	"""
	Prints a message to the console when bot comes online
	:return: None
	"""
	print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
	"""
	Reads message for key word to prompt bot to respond
	:param message: the text of the most recent message
	"""
	#Do nothing if message came from this bot or message was not posted in a channel the bot should respond to
	if message.author == client.user or message.channel.id not in CHANNEL_IDS_TO_MONITOR:
		return

	#Test code to ensure bot works
	if message.content.startswith(".hello"):
		await message.channel.send("Hello!")
#######################################################################
# Run App
#######################################################################
client.run(TOKEN)