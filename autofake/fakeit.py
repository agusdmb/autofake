from collections.abc import Callable
from functools import wraps
from typing import Optional

from .backend import Backend, InMemoryBackend
from .models import Mode, Record


class FakeIt:
    def __init__(self, mode: Mode = Mode.PRODUCTION, backend: Optional[Backend] = None):
        self._mode = mode
        self._backend = backend or InMemoryBackend()

    def _production_mode(self, function: Callable):
        return function

    def _fake_mode(self, function: Callable, name: str) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs):
            return self._backend.get_result(name, *args, **kwargs)

        return wrapper

    def _record_mode(self, function: Callable, name: str) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            record = Record(args=args, kwargs=kwargs, result=result)
            self._backend.record_call(name, record)
            return result

        return wrapper

    def __call__(self, name: str):
        def outter_wrapper(function: Callable):
            if self._mode == Mode.PRODUCTION:
                return self._production_mode(function)

            if self._mode == Mode.FAKE:
                return self._fake_mode(function, name)

            if self._mode == Mode.RECORD:
                return self._record_mode(function, name)

            raise ValueError(f"Unkown mode {self._mode}")

        return outter_wrapper
