from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
from typing import Any, Optional, Tuple


class Mode(Enum):
    RECORD = auto()
    FAKE = auto()
    PRODUCTION = auto()


@dataclass
class Record:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)
    result: Any = None


class Backend(ABC):
    @abstractmethod
    def record_call(self, name: str, record: Record):
        ...

    @abstractmethod
    def get_result(self, name: str, record: Record) -> Any:
        ...


class InMemory(Backend):
    def __init__(self):
        self._records = defaultdict(list)

    def record_call(self, name: str, record: Record):
        self._records[name].append(record)

    def get_result(self, name: str, *args, **kwargs) -> Any:
        for record in self._records[name]:
            if record.args == args and record.kwargs == kwargs:
                return record.result
        raise ValueError("Record not found")


class Inspector:
    def __init__(self, mode: Mode = Mode.PRODUCTION, backend: Optional[Backend] = None):
        self._records: dict[str, list[Record]] = defaultdict(list)
        self._mode = mode
        self._backend = backend or InMemory()

    def _production_mode(self, function: Callable):
        return function

    def _fake_mode(self, function: Callable, name: str):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return self.get_result(name, *args, **kwargs)

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
                self._backend.record_call(name, record)
                self._records[name].append(record)
                return result

            return wrapper

        return outter_wrapper

    def get_result(self, name: str, *args, **kwargs) -> Any:
        return self._backend.get_result(name, *args, **kwargs)
