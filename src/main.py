import logging
from typing import List, Dict
from typing import Tuple
from urllib.parse import urlparse

import discord
from discord import option
from github import Github
from github.Repository import Repository

from github_repo import get_pending_review_pull_requests, pull_request_to_str
from settings import (
    ALLOWED_CHANNEL_IDS,
    DISCORD_TOKEN,
    GITHUB_TOKEN,
    ALLOWED_REPO_NAMES,
    ALLOWED_ORGANIZATIONS,
)

logger = logging.getLogger(__name__)

bot = discord.Bot()


def channel_is_allowed(channel_id) -> bool:
    if ALLOWED_CHANNEL_IDS:
        return str(channel_id) in ALLOWED_CHANNEL_IDS

    return True


def get_pending_reviews_message(repo):
    pending_pull_requests = get_pending_review_pull_requests(repo)
    if not pending_pull_requests:
        return None

    msg = "\n\n-----\n\n".join(
        map(pull_request_to_str, get_pending_review_pull_requests(repo))
    )

    title = f" **{repo.name}** ".center(40, "-")
    return "\n".join(
        [
            "",
            title,
            "",
            msg,
        ]
    )


async def get_repos(ctx: discord.AutocompleteContext) -> List[str]:
    """Returns a list of repos that begin with the characters entered so far."""
    if not channel_is_allowed(ctx.interaction.channel_id):
        return []
    return [repo for repo in repos.keys() if ctx.value.lower() in repo.lower()]


@bot.slash_command(name="pending_reviews")
@option("repo", description="Pick a repo!", autocomplete=get_repos)
async def pending_reviews(ctx, repo: str):
    if not channel_is_allowed(ctx.channel.id):
        await ctx.respond(
            f"Command not allowed in this channel (`id={ctx.channel.id}`)"
        )
        return

    try:
        repository = repos[repo]
    except KeyError:
        await ctx.respond(f"❌ Repository '{repo}' not found")
        return

    await ctx.defer()
    await ctx.respond(get_pending_reviews_message(repository))


@bot.event
async def on_application_command_error(
    ctx: discord.ApplicationContext,
    error: discord.DiscordException,
):
    logger.exception("Something went wrong")
    await ctx.respond("❌ Something went wrong")


def parse_pull_request_url(url: str) -> Tuple[str, int]:
    parsed_url = urlparse(url)
    repo_name, _, pr_number = parsed_url.path.removeprefix("/").rsplit("/", maxsplit=2)
    return repo_name, int(pr_number)


@bot.slash_command(name="pull_request")
@option("url", description="Pick a PR by number or url")
async def pending_reviews(ctx, url: str):
    if not channel_is_allowed(ctx.channel.id):
        await ctx.respond(
            f"Command not allowed in this channel (`id={ctx.channel.id}`)"
        )
        return

    repo_name, pr_number = parse_pull_request_url(url)
    try:
        repository = repos[repo_name]
    except KeyError:
        await ctx.respond(f"❌ Repository '{repo_name}' not found")
        return

    await ctx.defer()
    await ctx.respond(pull_request_to_str(repository.get_pull(pr_number)))


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong!")


def main():
    bot.run(DISCORD_TOKEN)


def get_repositories(github: Github) -> Dict[str, Repository]:
    if ALLOWED_ORGANIZATIONS:
        repos = {}
        for organization in ALLOWED_ORGANIZATIONS:
            repos.update(
                {
                    f"{organization}/{repo.name}": repo
                    for repo in github.get_organization(organization).get_repos()
                }
            )
    else:
        repos = {
            repo_name: github.get_repo(repo_name) for repo_name in ALLOWED_REPO_NAMES
        }

    return repos


if __name__ == "__main__":
    # Github
    github = Github(GITHUB_TOKEN)
    repos = get_repositories(github)
    print(f"Configured for repos: {','.join(repos.keys())}")

    # Discord
    print("Running bot")
    main()
    print("bot closed")
