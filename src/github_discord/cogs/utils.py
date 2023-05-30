from typing import Tuple
from urllib.parse import urlparse

from src.github_discord.cogs.settings import ALLOWED_CHANNEL_IDS


def channel_is_allowed(channel_id) -> bool:
    if ALLOWED_CHANNEL_IDS:
        return str(channel_id) in ALLOWED_CHANNEL_IDS

    return True


def parse_pull_request_url(url: str) -> Tuple[str, int]:
    parsed_url = urlparse(url)
    repo_name, _, pr_number = parsed_url.path.removeprefix("/").rsplit("/", maxsplit=2)
    return repo_name, int(pr_number)
