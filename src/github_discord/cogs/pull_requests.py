import re
from typing import List

import discord
from discord import option
from discord.ext import commands

from github_discord.cogs.utils import channel_is_allowed
from github_discord.cogs.utils import parse_pull_request_url
from github_discord.domain.githubb import PullRequest
from github_discord.domain.githubb import PullRequestRepository
from github_discord.domain.githubb import RepositoriesRepository


def find_pr_urls(text: str) -> list[dict[str, str]]:
    GITHUB_PR_URL_RE = re.compile(
        r"https?://(?:www\.)?github\.com/([^/\s]+)/([^/\s]+)/pull/(\d+)(?:[/?#][^\s>]*)?",
        re.IGNORECASE,
    )

    results = []
    for match in GITHUB_PR_URL_RE.finditer(text or ""):
        owner = match.group(1)
        repo = match.group(2)
        pr_number = match.group(3)
        url = match.group(0)

        results.append({"url": url, "owner": owner, "repo": repo, "pr": pr_number})
    return results


def get_embed_for_pull_request(pull_request: PullRequest) -> discord.Embed:
    if pull_request.description:
        title = (
            (pull_request.description or "").splitlines()[0] + "\n\n"
        ).removeprefix("# ")
    else:
        title = pull_request.title
    embed = discord.Embed(
        title=title,
        color=discord.Colour.blurple(),
        timestamp=pull_request.created_at,
        url=pull_request.url,
    )

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

    return embed


class PullRequestsReplier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repos = RepositoriesRepository().list()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        matches = find_pr_urls(message.content)
        for match in matches:
            repo_name, pr_number = f"{match['owner']}/{match['repo']}", match["pr"]

            try:
                repository = self.repos[repo_name]
            except KeyError:
                return

            pull_request = PullRequestRepository(repository).get(int(pr_number))
            embed = get_embed_for_pull_request(pull_request)
            await message.reply(embed=embed, mention_author=False)


class PullRequestsReplacer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repos = RepositoriesRepository().list()
        self._webhook_cache = {}

    async def get_webhook(self, channel: discord.TextChannel) -> discord.Webhook:
        if channel.id in self._webhook_cache:
            return self._webhook_cache[channel.id]

        webhooks = await channel.webhooks()
        webhook = discord.utils.get(webhooks, name="GithubBotReplacer")
        if webhook is None:
            webhook = await channel.create_webhook(name="GithubBotReplacer")

        self._webhook_cache[channel.id] = webhook
        return webhook

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        matches = find_pr_urls(message.content)
        if not matches:
            return

        # Use the first match or all of them?
        # The previous version processed all matches but could delete only once.
        # If there are multiple PRs in one message, it's better to show all embeds.
        embeds = []
        for match in matches:
            repo_name, pr_number = f"{match['owner']}/{match['repo']}", match["pr"]

            try:
                repository = self.repos[repo_name]
            except KeyError:
                continue

            pull_request = PullRequestRepository(repository).get(int(pr_number))
            embeds.append(get_embed_for_pull_request(pull_request))

        if not embeds:
            return

        # Attempt to use a webhook to mimic the user
        webhook = await self.get_webhook(message.channel)

        await webhook.send(
            content=message.content,
            embeds=embeds,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
        )
        await message.delete()


class PullRequestsCommand(commands.Cog):
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
        embed = get_embed_for_pull_request(pull_request)
        await ctx.respond(comment, embed=embed)
