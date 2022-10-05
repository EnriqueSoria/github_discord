import os
from typing import Any, List


def get_env_list(name: str, default: Any, split_by: str = ",") -> List[str]:
    try:
        value = os.environ[name]
        if value:
            return value.split(split_by)
    except KeyError:
        return default
