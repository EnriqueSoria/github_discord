from operator import attrgetter
from typing import Iterable, List

from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository


def has_pending_review(pull_request: PullRequest) -> bool:
    return "" in map(attrgetter("state"), pull_request.get_reviews())


def pull_request_is_ready(pull_request: PullRequest) -> bool:
    return not pull_request.draft


def get_label_names(pull_request: PullRequest) -> List[str]:
    return [label.name for label in pull_request.labels]


def get_pending_review_pull_requests(repo: Repository) -> Iterable[PullRequest]:
    pull_requests = repo.get_pulls(state="open", base="staging")

    pull_requests = filter(has_pending_review, pull_requests)
    pull_requests = filter(pull_request_is_ready, pull_requests)

    return pull_requests


def labels_to_str(labels: List[str]) -> str:
    return ", ".join([f"`{label}`" for label in labels])


def pull_request_to_str(pull_request: PullRequest) -> str:
    labels = labels_to_str(get_label_names(pull_request))
    return f"{pull_request.title} ({labels}) {pull_request.url}"
