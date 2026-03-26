import logging
import os

import discord
from dotenv import load_dotenv

from github_discord.cogs.pull_requests import PullRequestsReplacer
from github_discord.github_service import GithubService
from utils import get_env_list

load_dotenv()

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
    github_service = GithubService(
        github_token=os.environ["GITHUB_TOKEN"],
        allowed_repositories=get_env_list("ALLOWED_REPO_NAMES", default=None),
        allowed_organizations=get_env_list("ALLOWED_ORGANIZATIONS", default=None),
    )

    repos = github_service.list_repositories()
    print(f"Configured for repos: {','.join(repos.keys())}")

    print("Running bot...")
    bot.add_cog(PullRequestsReplacer(bot, github_service))
    bot.run(os.environ["DISCORD_TOKEN"])
    print("Bot closed")


if __name__ == "__main__":
    main()
