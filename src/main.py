from dotenv import load_dotenv

load_dotenv()


import logging
import os
import discord

from github_discord.cogs.pull_requests import PullRequests
from github_discord.domain.githubb import RepositoriesRepository


logger = logging.getLogger(__name__)
bot = discord.Bot()


@bot.event
async def on_application_command_error(
    ctx: discord.ApplicationContext,
    error: discord.DiscordException,
):
    logger.error(f"Something went wrong {error}", exc_info=error)
    await ctx.respond("❌ Something went wrong")


def main():
    bot.add_cog(PullRequests(bot))
    bot.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    repos = RepositoriesRepository().list()
    print(f"Configured for repos: {','.join(repos.keys())}")

    # Discord
    print("Running bot")
    main()
    print("bot closed")
