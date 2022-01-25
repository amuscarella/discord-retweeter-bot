#######################################################################
# config.py for discord retweeter
# contains constants & strings for easy access/modification
# Authors: Christopher J. Clayton II (Github: ChristopherClayton) &
#          Antonio D. Muscarella (Github: amuscarella)
#######################################################################
#Discord parameters
DISCORD_TOKEN_FNAME = "token.txt" #filepath to Discord bot token
TARGET_CHANNEL = 930511442006921257 #channel ID for bot to monitor

#Twitter parameters
TWITTER_TOKEN_FNAME = "twitter_token.txt" #filepath to Twitter API Bearer token
TWITTER_STREAM_URL = "https://api.twitter.com/2/tweets/search/stream" #Twitter Stream URL from Twitter API 
TWITTER_STREAM_RULES_URL = "https://api.twitter.com/2/tweets/search/stream/rules" #Twitter Stream rules URL from Twitter API
TWITTER_ACCOUNT_NAME = "bstategames" #the full name of the twitter account the bot should monitor
TWITTER_STREAM_RULES = [{"value": "from:{}".format(TWITTER_ACCOUNT_NAME)}] #-is:retweet the rules for the twitter stream
TWITTER_ACCOUNT_URL_PREFIX = "https://twitter.com/{}/status/".format(TWITTER_ACCOUNT_NAME) #the url prefix to reference the statuses of the account the bot is monitoring