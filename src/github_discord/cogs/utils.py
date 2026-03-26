from typing import Tuple
from urllib.parse import urlparse


def parse_pull_request_url(url: str) -> Tuple[str, int]:
    try:
        parsed_url = urlparse(url)
        _, user, repo_name, _, pr_number, *_ = parsed_url.path.split("/")
        return f"{user}/{repo_name}", int(pr_number)
    except Exception as e:
        raise ValueError(f"Invalid pull request URL: {url}") from e
