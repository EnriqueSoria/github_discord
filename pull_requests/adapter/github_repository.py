from __future__ import annotations

from operator import attrgetter
from typing import List

from github import Github, PullRequest as GithubPullRequest

from pull_requests.domain.pull_request import PullRequest
from pull_requests.domain.pull_request_repository import PullRequestRepository


class GithubPullRequestRepository(PullRequestRepository):
    def __init__(self, token: str, repository_name: str):
        self.client = Github(token)
        self.repository = self.client.get_repo(repository_name)

    @staticmethod
    def _review_is_pending(pull_request: GithubPullRequest) -> bool:
        review_states = map(attrgetter("state"), pull_request.get_reviews())
        return "APPROVED" not in review_states

    @staticmethod
    def _pull_request_is_ready(pull_request: GithubPullRequest) -> bool:
        return not pull_request.draft

    def review_pending(self) -> List[PullRequest]:
        """ Returns pull requests with pending reviews """
        pulls = self.repository.get_pulls(state="open", base="staging")

        return [
            pull
            for pull in pulls
            if self._pull_request_is_ready(pull) and self._review_is_pending(pull)
        ]
