from collections.abc import Callable
from enum import Enum, auto
from functools import wraps
from typing import Any, Optional

from inspector.backend import Backend, InMemory
from inspector.models import Record


class Mode(Enum):
    RECORD = auto()
    FAKE = auto()
    PRODUCTION = auto()


class Inspector:
    def __init__(self, mode: Mode = Mode.PRODUCTION, backend: Optional[Backend] = None):
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
                return result

            return wrapper

        return outter_wrapper

    def get_result(self, name: str, *args, **kwargs) -> Any:
        return self._backend.get_result(name, *args, **kwargs)
