import discord
from discord.ext import commands
from github import Github

from github_repo import get_pending_review_pull_requests, pull_request_to_str
from settings import GITHUB_REPO_NAME, DISCORD_TOKEN, GITHUB_TOKEN

# Discord
client = discord.Client()
bot = commands.Bot(command_prefix="$")

# Github
github = Github(GITHUB_TOKEN)
repo = github.get_repo(GITHUB_REPO_NAME)


@bot.command()
async def pending_reviews(ctx):
    message = "\n".join(map(pull_request_to_str, get_pending_review_pull_requests(repo)))
    await ctx.send(message)


client.run(DISCORD_TOKEN)
