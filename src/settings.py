import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ALLOWED_REPO_NAMES = os.environ.get("ALLOWED_REPO_NAMES", "*").split(",")
ALLOWED_ORGANIZATIONS = os.environ.get("ALLOWED_ORGANIZATIONS", "").split(",")
ALLOWED_CHANNEL_IDS = os.environ.get("ALLOWED_CHANNEL_IDS", "*").split(",")
