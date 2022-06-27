import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class PullRequest:
    title: str
    is_draft: bool
    labels: List[str]
    url: str
    created_at: datetime.datetime

    def __str__(self):
        return "\n".join(
            [
                f"💬 {self.title}",
                f"🏷 {','.join(self.labels)}",
                f"🔗 {self.url}",
            ]
        )

    def __lt__(self, other):
        if not isinstance(other, PullRequest):
            raise ValueError("Can only compare between PR instances")
        return self.created_at < other.created_at
