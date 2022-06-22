import discord
from discord.ext import commands
from github import Github

from github_repo import get_pending_review_pull_requests, pull_request_to_str
from settings import ALLOWED_CHANNEL_IDS, DISCORD_TOKEN, GITHUB_REPO_NAME, GITHUB_TOKEN

client = discord.Client()
bot = commands.Bot(command_prefix="$")


def channel_is_allowed(channel_id) -> bool:
    if "*" in ALLOWED_CHANNEL_IDS:
        return True

    return str(channel_id) in ALLOWED_CHANNEL_IDS


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@client.event
async def on_message(message):
    if not channel_is_allowed(message.channel.id):
        return

    if message.content == "$pending_reviews":
        await message.delete()
        await message.channel.send(get_pending_reviews_message(repo))


def get_pending_reviews_message(repo):
    pending_pull_requests = get_pending_review_pull_requests(repo)
    if not pending_pull_requests:
        return None

    msg = "\n-----\n".join(
        map(pull_request_to_str, get_pending_review_pull_requests(repo))
    )

    separator = "=" * 23
    return f"{separator}\n**PRs with code review pending:**\n{separator}\n\n{msg}"


@bot.command()
async def pending_reviews(ctx):
    await ctx.send(get_pending_reviews_message(repo))


if __name__ == "__main__":
    # Github
    github = Github(GITHUB_TOKEN)
    repo = github.get_repo(GITHUB_REPO_NAME)

    # Discord
    print("Running client")
    client.run(DISCORD_TOKEN)
    print("client closed")
