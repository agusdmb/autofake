from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
from typing import Any, Tuple


class Mode(Enum):
    RECORD = auto()
    FAKE = auto()
    PRODUCTION = auto()


@dataclass
class Record:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)
    result: Any = None


class Inspector:
    def __init__(
        self,
        mode: Mode = Mode.PRODUCTION,
        backend: Callable[[Record], None] = lambda _: None,
    ):
        self._records: dict[str, list[Record]] = defaultdict(list)
        self._mode = mode
        self._backend = backend

    def load_records(self, records: dict[str, list[Record]]):
        self._records = records

    def _production_mode(self, function: Callable):
        return function

    def _fake_mode(self, function: Callable, name: str):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return self._get_result_from(name, *args, **kwargs)

        return wrapper

    def __call__(self, name: str):
        def outter_wrapper(function: Callable):
            if self._mode == Mode.PRODUCTION:
                return self._production_mode(function)

            if self._mode == Mode.FAKE:
                return self._fake_mode(function, name)

            @wraps(function)
            def wrapper(*args, **kwargs):
                result = function(*args, **kwargs)
                record = Record(args=args, kwargs=kwargs, result=result)
                self._backend(record)
                self._records[name].append(record)
                return result

            return wrapper

        return outter_wrapper

    def get_records_of(self, name: str) -> list[Record]:
        return self._records[name]

    def get_records(self) -> dict[str, list[Record]]:
        return self._records

    def _get_result_from(self, name: str, *args, **kwargs) -> Any:
        for record in self._records[name]:
            if record.args == args and record.kwargs == kwargs:
                return record.result
        raise ValueError("Record not found")
