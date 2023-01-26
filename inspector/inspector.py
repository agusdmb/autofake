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

    def __call__(self, name):
        def outter_wrapper(function):
            def wrapper(*args, **kwargs):
                result = function(*args, **kwargs)
                self._records[name].append(
                    Record(args=list(args), kwargs=kwargs, result=result)
                )
                return result

            return wrapper

        return outter_wrapper

    def get_records_of(self, name):
        return self._records[name]
