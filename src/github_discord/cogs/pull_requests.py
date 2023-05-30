from typing import List

import discord
from discord import option
from discord.ext import commands


from src.github_discord.cogs.utils import channel_is_allowed
from src.github_discord.cogs.utils import parse_pull_request_url
from src.github_discord.domain.githubb import PendingReviewFormatter
from src.github_discord.domain.githubb import PullRequestFormatter
from src.github_discord.domain.githubb import PullRequestRepository
from src.github_discord.domain.githubb import RepositoriesRepository


class PullRequests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repos = RepositoriesRepository().list()

    async def get_repos(self, ctx: discord.AutocompleteContext) -> List[str]:
        """Returns a list of repos that begin with the characters entered so far."""
        if not channel_is_allowed(ctx.interaction.channel_id):
            return []
        return [repo for repo in self.repos.keys() if ctx.value.lower() in repo.lower()]

    @discord.slash_command(name="pending_reviews")
    @option("repo", description="Pick a repo!", autocomplete=get_repos)
    async def pending_reviews(self, ctx, repo: str):
        if not channel_is_allowed(ctx.channel.id):
            await ctx.respond(
                f"Command not allowed in this channel (`id={ctx.channel.id}`)"
            )
            return

        try:
            repository = self.repos[repo]
        except KeyError:
            await ctx.respond(f"❌ Repository '{repo}' not found")
            return

        await ctx.defer()
        pull_requests = PullRequestRepository(repository).list()
        await ctx.respond(PendingReviewFormatter()(pull_requests.items()))

    @discord.slash_command(name="pull_request")
    @option("url", description="Pick a PR by number or url")
    async def pending_reviews(self, ctx, url: str):
        if not channel_is_allowed(ctx.channel.id):
            await ctx.respond(
                f"Command not allowed in this channel (`id={ctx.channel.id}`)"
            )
            return

        repo_name, pr_number = parse_pull_request_url(url)
        try:
            repository = self.repos[repo_name]
        except KeyError:
            await ctx.respond(f"❌ Repository '{repo_name}' not found")
            return

        await ctx.defer()

        pull_request = PullRequestRepository(repository).get(pr_number)
        await ctx.respond(PullRequestFormatter()(pull_request))
