#######################################################################
# Discord Retweeter
# Authors: Antonio Muscarella (Github: amuscarella)
#######################################################################
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import bot
import threading
import requests
import json
import time
#Local imports
from config import *
#######################################################################
# Intents Declaration & Client Initialization
#######################################################################
#read token
TOKEN = open(TOKEN_FNAME, 'r').readline()
TWITTER_TOKEN = open(TWITTER_TOKEN_FNAME, 'r').readline()

#declare discord intents & initialize client
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents = intents)
#######################################################################
# Twitter Auth
#######################################################################
bearer_token = TWITTER_TOKEN

search_url = "https://api.twitter.com/2/tweets/search/recent"

query_params = {'query': 'from:bstategames -is:retweet','tweet.fields': 'author_id', 'max_results': 10}
#######################################################################
# Twitter Functions
#######################################################################
def bearer_oauth(r):
	r.headers["Authorization"] = f"Bearer {bearer_token}"
	return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.text

def parse_json_response(response_as_json):
    print(response_as_json)
    data = response_as_json["data"]
    print(data)
    id = data["id"]
    return id

def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [{"value": "from:bstategames"}]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet_id = parse_json_response(json_response)
            link = "https://twitter.com/bstategames/status/" + tweet_id
            return(link)

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

# @client.event
# async def on_message(message):
# 	"""
# 	Reads message for key word to prompt bot to respond
# 	:param message: the text of the most recent message
# 	"""
# 	#Do nothing if message came from this bot or message was not posted in a channel the bot should respond to
# 	if message.author == client.user or message.channel.id not in CHANNEL_IDS_TO_MONITOR:
# 		return

# 	#Test code to ensure bot works
# 	if message.content.startswith(".hello"):
# 		json = connect_to_endpoint(search_url, query_params)
# 		tweet_id = parse_json_response(json)
# 		link = "https://twitter.com/bstategames/status/" + tweet_id
# 		await message.channel.send(link)

async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(id=930511442006921257) # replace with channel_id
    while not client.is_closed():
        link = twitter_stream()
        if (link):
            await channel.send(link)
        await asyncio.sleep(60) # task runs every 60 seconds

def twitter_stream():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    link = get_stream(set)
    return(link)
#######################################################################
# Run App
#######################################################################
client.loop.create_task(my_background_task())
client.run(TOKEN)