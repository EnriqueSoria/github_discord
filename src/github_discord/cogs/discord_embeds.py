import discord

from github_discord.github_service import PullRequest


def get_embed_for_pull_request(pull_request: PullRequest) -> discord.Embed:
    if pull_request.description:
        title = ((pull_request.description or "").splitlines()[0] + "\n\n").removeprefix("# ")
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
