from operator import attrgetter
from typing import Iterable, List

from github.PullRequest import PullRequest
from github.Repository import Repository


def review_is_pending(pull_request: PullRequest) -> bool:
    review_states = map(attrgetter("state"), pull_request.get_reviews())
    return "APPROVED" not in review_states


def pull_request_is_ready(pull_request: PullRequest) -> bool:
    return not pull_request.draft


def get_label_names(pull_request: PullRequest) -> List[str]:
    return [label.name for label in pull_request.labels]


def get_pending_review_pull_requests(repo: Repository) -> Iterable[PullRequest]:
    pull_requests = repo.get_pulls(state="open", base="staging")

    pr_filters = (
        pull_request_is_ready,
        review_is_pending,
    )

    for pr_filter in pr_filters:
        pull_requests = filter(pr_filter, pull_requests)

    return pull_requests


def labels_to_str(labels: List[str]) -> str:
    return ", ".join([f"`{label}`" for label in labels])


def pull_request_to_str(pull_request: PullRequest) -> str:
    labels = labels_to_str(get_label_names(pull_request))
    return "\n".join(
        [
            f"💬 {pull_request.title}",
            f"🏷 {labels}",
            f"🔗 {pull_request.html_url}",
        ]
    )
