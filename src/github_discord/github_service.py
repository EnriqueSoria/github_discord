import datetime
import functools
from dataclasses import dataclass
from typing import Set

import github


@dataclass(frozen=True)
class Repository:
    name: str


@dataclass(frozen=True)
class PullRequest:
    repository: Repository
    description: str
    number: int
    title: str
    labels: Set[str]
    created_at: datetime.datetime
    draft: bool
    url: str


def _build_pull_request_from_github_pull(
    repository: Repository, pull: github.PullRequest
) -> PullRequest:
    return PullRequest(
        repository=repository,
        number=pull.number,
        title=pull.title,
        description=pull.body,
        labels={label.name for label in pull.labels},
        created_at=pull.created_at,
        draft=pull.draft,
        url=pull.html_url,
    )


class GithubService:
    def __init__(
        self,
        github_token: str,
        allowed_repositories: list[str] | None = None,
        allowed_organizations: list[str] | None = None,
    ):
        self.github = github.Github(github_token)
        self.allowed_organizations = allowed_organizations
        self.allowed_repositories = allowed_repositories

        if self.allowed_organizations is None and self.allowed_repositories is None:
            raise ValueError(
                "You must specify at least one organization if allowing all repos"
            )

    @functools.lru_cache
    def list_repositories(self) -> dict[str, Repository]:
        if self.allowed_organizations:
            repos = []
            for organization in self.allowed_organizations:
                repos.extend(self.github.get_organization(organization).get_repos())
        else:
            repos = [
                self.github.get_repo(repo_name)
                for repo_name in self.allowed_repositories
            ]

        return {repo.full_name: Repository(name=repo.full_name) for repo in repos}

    def get_repository(self, full_name: str) -> Repository:
        return self.list_repositories()[full_name]

    def list_pull_requests(self, repository: Repository) -> dict[int, PullRequest]:
        repository = self.github.get_repo(repository.name)
        pull_requests = repository.get_pulls()

        return {
            pull_request.number: _build_pull_request_from_github_pull(
                repository, pull_request
            )
            for pull_request in pull_requests
        }

    def get_pull_request(self, repository: Repository, number: int) -> PullRequest:
        repository = self.github.get_repo(repository.name)
        pull_request = repository.get_pull(number)

        return _build_pull_request_from_github_pull(repository, pull_request)
