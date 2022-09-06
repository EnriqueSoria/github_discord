import asyncio

import discord
from discord.ext import commands
from github import Github

from github_repo import get_pending_review_pull_requests, pull_request_to_str
from settings import ALLOWED_CHANNEL_IDS, DISCORD_TOKEN, GITHUB_REPO_NAME, GITHUB_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


def channel_is_allowed(channel_id) -> bool:
    if "*" in ALLOWED_CHANNEL_IDS:
        return True

    return str(channel_id) in ALLOWED_CHANNEL_IDS


def get_pending_reviews_message(repo):
    pending_pull_requests = get_pending_review_pull_requests(repo)
    if not pending_pull_requests:
        return None

    msg = "\n-----\n".join(
        map(pull_request_to_str, get_pending_review_pull_requests(repo))
    )

    separator = "=" * 23
    return f"{separator}\n**PRs with code review pending:**\n{separator}\n\n{msg}"


@bot.command(name="pending_reviews")
async def pending_reviews(ctx):
    if not channel_is_allowed(ctx.channel.id):
        await ctx.channel.send(
            f"Command not allowed in this channel (`id={ctx.channel.id}`)"
        )
        return

    await ctx.channel.send(get_pending_reviews_message(repo))


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong!")


async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    # Github
    print(f"Configured for repo: {GITHUB_REPO_NAME}")
    github = Github(GITHUB_TOKEN)
    repo = github.get_repo(GITHUB_REPO_NAME)

    # Discord
    print("Running bot")
    asyncio.run(main())
    print("bot closed")
