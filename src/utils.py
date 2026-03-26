import os
from typing import Any, TypeVar

T = TypeVar("T")


def get_env_list(name: str, default: T, split_by: str = ",") -> list[str] | T:
    try:
        value = os.environ[name]
        if value:
            return value.split(split_by)
    except KeyError:
        return default
