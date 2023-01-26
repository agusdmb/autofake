from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Record:
    args: list[Any] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)
    result: Any = None


class Inspector:
    def __init__(self):
        self._records = defaultdict(list)

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            self._records[function.__class__].append(
                Record(args=list(args), kwargs=kwargs, result=result)
            )
            return result

        return wrapper

    def get_records_of(self, function):
        return self._records[function.__class__]
