from operator import attrgetter
from typing import Iterable, List

from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository

from pull_requests.domain.pull_request import PR


class PRAdapter:
    @classmethod
    def from_pull_request(cls, pull_request: PullRequest) -> PR:
        return PR(
            title=pull_request.title,
            is_draft=pull_request.draft,
            labels=[label.name for label in pull_request.labels],
            url=pull_request.html_url,
            created_at=pull_request.created_at,
        )


class GithubService:
    def __init__(self, token: str, repository_name: str):
        self.client = Github(token)
        self.repository = self.client.get_repo(repository_name)

    def get_pending_review_pull_requests(self, repo: Repository) -> List[PR]:
        ...



def review_is_pending(pull_request: PullRequest) -> bool:
    review_states = map(attrgetter("state"), pull_request.get_reviews())
    return "APPROVED" not in review_states


def pull_request_is_ready(pull_request: PullRequest) -> bool:
    return not pull_request.draft


def get_pending_review_pull_requests(repo: Repository) -> Iterable[PullRequest]:
    pull_requests = repo.get_pulls(state="open", base="staging")

    pr_filters = (
        pull_request_is_ready,
        review_is_pending,
    )

    for pr_filter in pr_filters:
        pull_requests = filter(pr_filter, pull_requests)

    return pull_requests


def pull_request_to_str(pull_request: PullRequest) -> str:
    return str(PRAdapter.from_pull_request(pull_request))
