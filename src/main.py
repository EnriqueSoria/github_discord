from dotenv import load_dotenv

load_dotenv()

import re
import logging
import os
import discord

from github_discord.cogs.pull_requests import PullRequestsReplier, PullRequestsReplacer
from github_discord.domain.githubb import PullRequestRepository
from github_discord.domain.githubb import RepositoriesRepository
from github_discord.cogs.utils import parse_pull_request_url

logger = logging.getLogger(__name__)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_application_command_error(
    ctx: discord.ApplicationContext,
    error: discord.DiscordException,
):
    logger.error(f"Something went wrong {error}", exc_info=error)
    await ctx.respond("❌ Something went wrong")


def main():
    bot.add_cog(PullRequestsReplacer(bot))
    bot.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    repos = RepositoriesRepository().list()
    print(f"Configured for repos: {','.join(repos.keys())}")

    # Discord
    print("Running bot")
    main()
    print("bot closed")
