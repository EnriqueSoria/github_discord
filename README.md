# GithubDiscordBot
A command for a discord bot to send private pull requests with a rich preview in Discord.

This repo contains:
 - Multiple installable cogs for your Discord bot:
    - `PullRequestsReplacer`: Automatically replaces GitHub PR URLs with a rich preview using a webhook (mimics the original user).
    - `PullRequestsReplier`: Responds to GitHub PR URLs with a rich preview.
    - `PullRequestsCommand`: Provides the `/pull_request` slash command.
 - A simple Discord bot that already includes the `PullRequestsReplacer` cog.

![img.png](img.png)


## How to run the bot
 - Populate .env: `cp .env.sample .env`
 - Fill the .env with as desired (requires `GITHUB_TOKEN` and either `ALLOWED_REPO_NAMES` or `ALLOWED_ORGANIZATIONS`)
 - Run bot: `make`

## How to install it on your bot
Install the library:
````shell
pip install https://github.com/EnriqueSoria/github_discord.git
````

Add a cog to your bot:
```python
from github_discord.cogs.pull_requests import PullRequestsReplacer
from github_discord.github_service import GithubService

github_service = GithubService(
    github_token="YOUR_GITHUB_TOKEN",
    allowed_repositories=["owner/repo1", "owner/repo2"],
)

bot = discord.Bot()
bot.add_cog(PullRequestsReplacer(bot, github_service))
```

## Use it (in discord)
If you are using `PullRequestsReplacer` or `PullRequestsReplier`, simply paste a GitHub Pull Request URL in a message.

If you are using `PullRequestsCommand`:
`/pull_request url:https://github.com/owner/repo/pull/123`

