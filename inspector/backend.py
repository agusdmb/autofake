from collections import defaultdict
from typing import Any, Protocol

from inspector.models import Record


class Backend(Protocol):
    def record_call(self, name: str, record: Record):
        ...

    def get_result(self, name: str, record: Record) -> Any:
        ...


class InMemory:
    def __init__(self):
        self._records = defaultdict(list)

    def record_call(self, name: str, record: Record):
        self._records[name].append(record)

    def get_result(self, name: str, *args, **kwargs) -> Any:
        for record in self._records[name]:
            if record.args == args and record.kwargs == kwargs:
                return record.result
        raise ValueError("Record not found")
