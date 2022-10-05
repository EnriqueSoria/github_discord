from github import Github

from settings import GITHUB_TOKEN
from src.main import get_pending_reviews_message, get_repositories

if __name__ == "__main__":
    github = Github(GITHUB_TOKEN)

    repos = get_repositories(github)

    print(f"Repos: {', '.join(repos.keys())}")
    repo = list(repos.values())[0]
    print(get_pending_reviews_message(repo))
