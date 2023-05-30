import logging
import os

import discord

from src.github_discord.cogs.pull_requests import PullRequests
from src.github_discord.domain.githubb import RepositoriesRepository

logger = logging.getLogger(__name__)

bot = discord.Bot()


@bot.event
async def on_application_command_error(
    ctx: discord.ApplicationContext,
    error: discord.DiscordException,
):
    logger.exception(f"Something went wrong {error}")
    await ctx.respond("❌ Something went wrong")


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong!")


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
