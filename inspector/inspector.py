from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class Mode(Enum):
    RECORD = auto()
    FAKE = auto()
    PRODUCTION = auto()


@dataclass
class Record:
    args: list[Any] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)
    result: Any = None


class Inspector:
    def __init__(self, mode: Mode):
        self._records: dict[str, list[Record]] = defaultdict(list)
        self._mode = mode

    def load_records(self, records: dict[str, list[Record]]):
        self._records = records

    def _production_mode(self, function: Callable):
        return function

    def __call__(self, name: str):
        def outter_wrapper(function: Callable):
            if self._mode == Mode.PRODUCTION:
                return self._production_mode(function)

            def wrapper(*args, **kwargs):
                result = function(*args, **kwargs)
                self._records[name].append(
                    Record(args=list(args), kwargs=kwargs, result=result)
                )
                return result

            return wrapper

        return outter_wrapper

    def get_records_of(self, name: str) -> list[Record]:
        return self._records[name]

    def get_records(self) -> dict[str, list[Record]]:
        return self._records
