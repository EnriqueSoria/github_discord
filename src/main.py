from typing import List

import discord
from discord import option
from github import Github

from github_repo import get_pending_review_pull_requests, pull_request_to_str
from settings import (
    ALLOWED_CHANNEL_IDS,
    DISCORD_TOKEN,
    GITHUB_TOKEN,
    ALLOWED_REPO_NAMES,
)

bot = discord.Bot()


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
    return f"{separator}\n**{repo.name}:**\n{separator}\n\n{msg}"


async def get_repos(ctx: discord.AutocompleteContext) -> List[str]:
    """Returns a list of repos that begin with the characters entered so far."""
    if not channel_is_allowed(ctx.interaction.channel_id):
        return []
    return [repo for repo in repos.keys() if repo.startswith(ctx.value.lower())]


@bot.slash_command(name="pending_reviews")
@option("repo", description="Pick a repo!", autocomplete=get_repos)
async def pending_reviews(ctx, repo: str):
    if not channel_is_allowed(ctx.channel.id):
        await ctx.respond(
            f"Command not allowed in this channel (`id={ctx.channel.id}`)"
        )
        return

    await ctx.respond(get_pending_reviews_message(repos[repo]))


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong!")


def main():
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    # Github
    github = Github(GITHUB_TOKEN)

    repos = ALLOWED_REPO_NAMES
    if "*" in ALLOWED_REPO_NAMES:
        repos = {repo.name: repo for repo in github.get_repos()}
    else:
        repos = {
            repo_name: github.get_repo(repo_name) for repo_name in ALLOWED_REPO_NAMES
        }

    print(f"Configured for repos: {','.join(repos.keys())}")

    # Discord
    print("Running bot")
    main()
    print("bot closed")
