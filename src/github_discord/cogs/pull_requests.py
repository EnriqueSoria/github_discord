from typing import List

import discord
from discord import option
from discord.ext import commands
from github_discord.cogs.utils import channel_is_allowed
from github_discord.cogs.utils import parse_pull_request_url
from github_discord.domain.githubb import PullRequestRepository
from github_discord.domain.githubb import RepositoriesRepository


class PullRequests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repos = RepositoriesRepository().list()

    async def get_repos(self, ctx: discord.AutocompleteContext) -> List[str]:
        """Returns a list of repos that begin with the characters entered so far."""
        if not channel_is_allowed(ctx.interaction.channel_id):
            return []
        return [repo for repo in self.repos.keys() if ctx.value.lower() in repo.lower()]

    @discord.slash_command(name="pull_request", allowed_mentions=True)
    @option("url", description="Add a pull request URL")
    @option("comment", description="Add an additional comment")
    async def pull_request(self, ctx, url: str, comment: str = ""):
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

        embed = discord.Embed(
            title=pull_request.title,
            description=(pull_request.description or "") + "\n\n",
            color=discord.Colour.blurple(),
            timestamp=pull_request.created_at,
            url=pull_request.url,
        )

        embed.add_field(name="🔗 URL", value=pull_request.url, inline=False)
        if pull_request.labels:
            embed.add_field(
                name="🏷 Labels",
                value=", ".join([f"`{label}`" for label in pull_request.labels]),
                inline=False,
            )

        embed.set_author(
            name=f"#{pull_request.number} on {pull_request.repository.name}",
            url=pull_request.url,
        )

        await ctx.respond(comment, embed=embed)
