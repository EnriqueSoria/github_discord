import datetime
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Set

import github
import humanize

from github_discord.cogs import settings
from github_discord.cogs.settings import ALLOWED_ORGANIZATIONS
from github_discord.cogs.settings import ALLOWED_REPO_NAMES
from github_discord.cogs.settings import GITHUB_TOKEN


@dataclass
class Repository:
    name: str


@dataclass
class PullRequest:
    repository: Repository
    number: int
    title: str
    labels: Set[str]
    created_at: datetime.datetime
    draft: bool
    url: str


class RepositoriesRepository:
    def __init__(self):
        self.github = github.Github(GITHUB_TOKEN)

    def list(self) -> Dict[str, Repository]:
        if ALLOWED_ORGANIZATIONS:
            repos = []
            for organization in ALLOWED_ORGANIZATIONS:
                repos.extend(self.github.get_organization(organization).get_repos())
        else:
            repos = [
                self.github.get_repo(repo_name) for repo_name in ALLOWED_REPO_NAMES
            ]

        return {repo.full_name: Repository(name=repo.full_name) for repo in repos}

    def get(self, name: str) -> Repository:
        return self.list()[name]

    def find(self, expression: str) -> List[Repository]:
        return [
            repo
            for repo_name, repo in self.list().items()
            if expression.casefold() in repo_name.casefold()
        ]


class PullRequestRepository:
    def __init__(self, repository: Repository):
        self.github = github.Github(GITHUB_TOKEN)
        self.repository = repository

    def list(self) -> Dict[str, PullRequest]:
        repository = self.github.get_repo(self.repository.name)
        pull_requests = repository.get_pulls(state="open")  # base=settings.BASE_BRANCH)

        return {
            pull_request.number: PullRequest(
                repository=self.repository,
                number=pull_request.number,
                title=pull_request.title,
                labels={label.name for label in pull_request.labels},
                created_at=pull_request.created_at,
                draft=pull_request.draft,
                url=pull_request.html_url,
            )
            for pull_request in pull_requests
        }

    def get(self, number) -> PullRequest:
        return self.list()[number]


class PullRequestFormatter:
    def __call__(self, pull_request: PullRequest) -> str:
        labels = ", ".join([f"`{label}`" for label in pull_request.labels])
        humanize.i18n.activate(settings.LOCALE)
        time_ago = humanize.naturaltime(
            datetime.datetime.now() - pull_request.created_at
        )
        return "\n".join(
            [
                f"**{pull_request.title}**",
                f"🏷 {labels}",
                f"🔗 {pull_request.url}",
                f"⏲ {time_ago}",
            ]
        )


class PendingReviewFormatter:
    """Format pull request to be shown in discord"""

    def __call__(self, pull_requests: List[PullRequest]):
        msg = "\n\n-----\n\n".join(map(PullRequestFormatter(), pull_requests))

        title = f" **{pull_requests[0].repository.name}** ".center(40, "-")
        return "\n".join(
            [
                "",
                title,
                "",
                msg,
            ]
        )
