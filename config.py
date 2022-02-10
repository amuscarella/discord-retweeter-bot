#######################################################################
# config.py for discord retweeter
# contains strings, constants, & string keys that map to config vars on Heroku 
# Authors: Christopher J. Clayton II (Github: ChristopherClayton) &
#          Antonio D. Muscarella (Github: amuscarella)
#######################################################################
#Discord parameters
DISCORD_TOKEN_KEY = "DISCORD_TOKEN" #config var key for Discord bot token
DISCORD_CHANNEL_KEY = "TARGET_CHANNEL" #channel ID for bot to monitor

#Twitter parameters
TWITTER_TOKEN_KEY = "TWITTER_TOKEN" #config var key for Twitter API Bearer token
TWITTER_ACCOUNT_NAME_KEY = "TWITTER_ACCOUNT_NAME" #config var key for the full name of the twitter account the bot should monitor
TWITTER_STREAM_URL = "https://api.twitter.com/2/tweets/search/stream" #Twitter Stream URL from Twitter API 
TWITTER_STREAM_RULES_URL = "https://api.twitter.com/2/tweets/search/stream/rules" #Twitter Stream rules URL from Twitter API