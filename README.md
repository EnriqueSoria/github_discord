# GithubDiscordBot
A command for a discord bot to send private pull requests with a rich preview in Discord.

This repo contains:
 - An installable cog, so you can include `/pull_request` command in your bot.
 - A simple Discord bot that already includes the `/pull_request` command.

![imatge](https://github.com/user-attachments/assets/570a02b4-14ce-48f7-9b38-753b05eb80e6)


## How to run the bot
 - Populate .env: `cp .env.sample .env`
 - Fill the .env with as desired
 - Run bot: `make`

## How to install it on your bot
Install the library:
````shell
pip install https://github.com/EnriqueSoria/github_discord.git
````

Add the cog to your bot:
```python
from github_discord.cogs.pull_requests import PullRequests

bot = discord.Bot()
bot.add_cog(PullRequests(bot))
```

## Use it (in discord)
Talk to your bot or add it to a group and send this message:
`/pending_reviews`

