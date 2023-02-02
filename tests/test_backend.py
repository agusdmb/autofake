import json
import tempfile

import pytest

from inspector.backend import JsonBackend
from inspector.exceptions import RecordNotFound
from inspector.models import Record


class TestJsonBackend:
    def test_json_backend_record(self):
        with tempfile.NamedTemporaryFile() as temp:
            record = Record(args=(3,), kwargs={"b": 4}, result=7)

            json_backend = JsonBackend(temp.name)
            json_backend.record_call("function", record)

            data = json.load(temp)
            assert data == {"function": {"args": [3], "kwargs": {"b": 4}, "result": 7}}

    def test_json_backend_get(self):
        with tempfile.NamedTemporaryFile() as temp:
            json_backend = JsonBackend(temp.name)
            json_backend.record_call(
                "function", Record(args=(3,), kwargs={"b": 4}, result=7)
            )
            assert json_backend.get_result("function", 3, b=4) == 7

    def test_json_backend_no_value(self):
        with tempfile.NamedTemporaryFile() as temp:
            json_backend = JsonBackend(temp.name)
            with pytest.raises(RecordNotFound):
                assert json_backend.get_result("function", 3, b=4) == 7
