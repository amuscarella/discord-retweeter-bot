# discord-retweeter-bot
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

A bot for posting tweets from an account on Twitter to a Discord channel. 

If you wish to deploying an instance of this bot, you need to complete the following steps:
1. Create a Discord bot using the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a Twitter auth token for a Twitter Stream using the [Twitter Developer API](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/introduction)
3. Invite your Discord bot to the server you wish to host it on.

To configure the bot to your specifications, set the following Config Vars for your app (in Heroku this can be accomplished in your app's Settings):
- `DISCORD_TOKEN` : the Discord token you generated for your bot
- `TARGET_CHANNEL` : the channel ID of the Discord channel you would like your bot to post to
- `TWITTER_ACCOUNT_NAME` : the full name of the twitter account you wish for the bot to follow (without the '@')
- `TWITTER_TOKEN` : the Twitter auth token you generated for the Twitter stream
    
This app was built on Heroku using the following resources for reference:
- [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Python on Heroku](https://devcenter.heroku.com/categories/python)
