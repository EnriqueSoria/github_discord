from github import Github

from settings import GITHUB_REPO_NAME, GITHUB_TOKEN

if __name__ == "__main__":
    github = Github(GITHUB_TOKEN)
    repo = github.get_repo(GITHUB_REPO_NAME)

    from main import get_pending_reviews_message

    print(get_pending_reviews_message(repo))
