from __future__ import annotations

from typing import List

from pull_requests.domain.pull_request import PullRequest
from pull_requests.domain.pull_request_repository import PullRequestRepository


class InMemoryPullRequestRepository(PullRequestRepository):
    def __init__(self):
        self.pull_requests = []

    def add(self, pull_request: PullRequest) -> PullRequest:
        self.pull_requests.append(pull_request)
        return pull_request

    def all(self) -> List[PullRequest]:
        return self.pull_requests
