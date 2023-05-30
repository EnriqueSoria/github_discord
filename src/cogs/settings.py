import os
from typing import Any, List
from dotenv import load_dotenv


def get_env_list(name: str, default: Any, split_by: str = ",") -> List[str]:
    try:
        value = os.environ[name]
        if value:
            return value.split(split_by)
    except KeyError:
        return default


load_dotenv()

LOCALE = os.environ.get("LOCALE", "es_ES")

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ALLOWED_REPO_NAMES = get_env_list("ALLOWED_REPO_NAMES", None)
ALLOWED_ORGANIZATIONS = get_env_list("ALLOWED_ORGANIZATIONS", None)
ALLOWED_CHANNEL_IDS = get_env_list("ALLOWED_CHANNEL_IDS", None)
BASE_BRANCH = os.environ.get("BASE_BRANCH", "main")


if not ALLOWED_ORGANIZATIONS and not ALLOWED_REPO_NAMES:
    raise ValueError("You must specify at least one organization if allowing all repos")
