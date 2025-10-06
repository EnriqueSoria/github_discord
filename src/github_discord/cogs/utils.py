from typing import Tuple
from urllib.parse import urlparse

from github_discord.cogs.settings import ALLOWED_CHANNEL_IDS


def channel_is_allowed(channel_id) -> bool:
    if ALLOWED_CHANNEL_IDS:
        return str(channel_id) in ALLOWED_CHANNEL_IDS

    return True


def parse_pull_request_url(url: str) -> Tuple[str, int]:
    try:
        parsed_url = urlparse(url)
        _, user, repo_name, _, pr_number, *_ = parsed_url.path.split("/")
        return f"{user}/{repo_name}", int(pr_number)
    except Exception as e:
        raise ValueError(f"Invalid pull request URL: {url}") from e
