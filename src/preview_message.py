from github import Github

from settings import GITHUB_TOKEN, ALLOWED_REPO_NAMES
from src.main import get_pending_reviews_message

if __name__ == "__main__":
    github = Github(GITHUB_TOKEN)
    repos = ALLOWED_REPO_NAMES
    if "*" in ALLOWED_REPO_NAMES:
        repos = {repo.name: repo for repo in github.get_repos()}
    else:
        repos = {
            repo_name: github.get_repo(repo_name) for repo_name in ALLOWED_REPO_NAMES
        }

    print(f"Repos: {', '.join(repos.keys())}")
    repo = list(repos.values())[0]
    print(get_pending_reviews_message(repo))
