import json
import pickle
from collections import defaultdict
from typing import Any, Protocol

from .exceptions import RecordNotFound
from .models import Record


class Backend(Protocol):
    def record_call(self, name: str, record: Record):
        ...

    def get_result(self, name: str, record: Record) -> Any:
        ...


class InMemoryBackend:
    def __init__(self):
        self._records = defaultdict(list)

    def record_call(self, name: str, record: Record):
        self._records[name].append(record)

    def get_result(self, name: str, *args, **kwargs) -> Any:
        for record in self._records[name]:
            if record.args == args and record.kwargs == kwargs:
                return record.result
        raise RecordNotFound("Record not found")


class PickleBackend:
    def __init__(self, filename):
        self._filename = filename
        self._records = defaultdict(list)

    def record_call(self, name: str, record: Record):
        self._records[name].append(record)
        self.dump()

    def dump(self):
        with open(self._filename, "wb") as file:
            pickle.dump(self._records, file)

    def get_result(self, name: str, *args, **kwargs) -> Any:
        if not self._records:
            self._load_records()

        for record in self._records[name]:
            if record.args == args and record.kwargs == kwargs:
                return record.result
        raise RecordNotFound("Record not found")

    def _load_records(self):
        try:
            with open(self._filename, "rb") as file:
                self._records = pickle.load(file)
        except EOFError:
            pass

    def __repr__(self):
        return f"<PickleBackend {self._filename}, {self._records}>"


class JSONBackend:
    def __init__(self, filename):
        self._filename = filename
        self._records = []

    def record_call(self, name: str, record: Record):
        with open(self._filename, "a") as file:
            json.dump({name: record.__dict__}, file)
            file.write("\n")

    def get_result(self, name: str, *args, **kwargs) -> Any:
        if not self._records:
            self._load_records()

        for raw_record in self._records:
            for func, record in raw_record.items():
                if func == name:
                    if record["args"] == list(args) and record["kwargs"] == kwargs:
                        return record["result"]

        raise RecordNotFound("Record not found")

    def _load_records(self):
        with open(self._filename) as file:
            for line in file:
                self._records.append(json.loads(line))
