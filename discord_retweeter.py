#!/usr/bin/python
#######################################################################
# Discord Retweeter
# A Discord bot for posting tweets from a specific Twitter account to a specific Discord channel.
# Authors: Christopher J. Clayton II (Github: ChristopherClayton) &
#          Antonio D. Muscarella (Github: amuscarella) 
#######################################################################
import asyncio
import json
import os

import discord
import requests

#Local imports
from config import *

#######################################################################
# Configuration, Intents Declaration & Client Initialization
#######################################################################
#read token
#DISCORD_TOKEN = open(DISCORD_TOKEN_FNAME, 'r').readline()
DISCORD_TOKEN = os.environ[DISCORD_TOKEN_KEY] # TODO: os.environ will replace token files
#TWITTER_TOKEN = open(TWITTER_TOKEN_FNAME, 'r').readline()
TWITTER_TOKEN = os.environ[TWITTER_TOKEN_KEY] # TODO: change these so they are secrets

#declare discord intents & initialize client
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents = intents)
#######################################################################
# Twitter Functions
#######################################################################
def bearer_oauth(r):
    '''
    Updates the bearer oauth with the token authorization
    :param r: the bearer oauth
    :return: the bearer oauth with the updated token
    '''
    r.headers["Authorization"] = f"Bearer {TWITTER_TOKEN}"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.text

def parse_json_response(response_as_json):
    '''
    Parses json response from the twitter stream.
    :param response_as_json: the response from the twitter stream as a json object
    :return: the id of the retrieved tweet
    '''
    #error handling - stream is not connected for some reason
    #if "data" not in response_as_json:
    #    print("ran into stream error")
    #    print(response_as_json)
    #    return
    print(response_as_json)
    data = response_as_json["data"]
    print(data)
    tweet_id = data["id"]
    return tweet_id

def get_rules():
    '''
    :return: the json dump of the response from the twitter stream
    '''
    response = requests.get(TWITTER_STREAM_RULES_URL, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()

def delete_all_rules(rules):
    '''
    Deletes rules for twitter stream monitoring
    :param rules: the specified rules for the twitter stream
    :return: None
    '''
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(TWITTER_STREAM_RULES_URL, auth=bearer_oauth, json=payload)
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    '''
    Sets rules for twitter stream to follow when monitoring
    :param delete:
    '''
    # You can adjust the rules if needed
    payload = {"add": TWITTER_STREAM_RULES}
    response = requests.post(TWITTER_STREAM_RULES_URL, auth=bearer_oauth, json=payload)
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(ruleset):
    '''
    Fetches the URL string of a tweet posted to a twitter stream.
    :param ruleset: the set of rules for the twitter stream to follow
    :return: the string of the URL for the tweet posted to the tream
    '''
    response = requests.get(TWITTER_STREAM_URL, auth=bearer_oauth, stream=True)
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

            #Error handling if no tweet was returned
            if tweet_id:
                link = TWITTER_ACCOUNT_URL_PREFIX + tweet_id
                return link

def initialize_twitter_stream():
    rules = get_rules()
    delete = delete_all_rules(rules)
    ruleset = set_rules(delete)
    return(ruleset)
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

async def post_twitter_link():
    """
    Waits for a new tweet to be posted from the account followed on the twitter stream,
    then posts link to desired discord channel. Waits 60 seconds to refresh.
    :return: None
    """
    await client.wait_until_ready()
    channel = client.get_channel(id=TARGET_CHANNEL)
    ruleset = initialize_twitter_stream()
    while not client.is_closed():
        try:
            link = get_stream(ruleset)
        except Exception as e:
            #Stream disconnect exception; print error and proceed through loop
            link = None
            print(e)
        #requests.exceptions.ChunkedEncodingError: ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))
        if (link):
            await channel.send(link)
        await asyncio.sleep(60) # task runs every 60 seconds
#######################################################################
# Run App
#######################################################################
client.loop.create_task(post_twitter_link())
client.run(DISCORD_TOKEN)