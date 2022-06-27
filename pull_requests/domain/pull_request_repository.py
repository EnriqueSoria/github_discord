from abc import ABC, abstractmethod
from typing import List

from pull_requests.domain.pull_request import PullRequest


class PullRequestRepository(ABC):

    @abstractmethod
    def review_pending(self) -> List[PullRequest]:
        ...



