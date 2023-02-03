import json
import pickle
import tempfile

import pytest

from autofake.backend import JSONBackend, PickleBackend
from autofake.exceptions import RecordNotFound
from autofake.models import Record


class TestJsonBackend:
    def test_json_backend_record(self):
        with tempfile.NamedTemporaryFile() as temp:
            record = Record(args=(3,), kwargs={"b": 4}, result=7)

            json_backend = JSONBackend(temp.name)
            json_backend.record_call("function", record)

            data = json.load(temp)
            assert data == {"function": {"args": [3], "kwargs": {"b": 4}, "result": 7}}

    def test_json_backend_get(self):
        with tempfile.NamedTemporaryFile() as temp:
            json_backend = JSONBackend(temp.name)
            json_backend.record_call(
                "function", Record(args=(3,), kwargs={"b": 4}, result=7)
            )
            assert json_backend.get_result("function", 3, b=4) == 7

    def test_json_backend_get_multi(self):
        with tempfile.NamedTemporaryFile() as temp:
            json_backend = JSONBackend(temp.name)
            json_backend.record_call(
                "function", Record(args=(3,), kwargs={"b": 4}, result=7)
            )
            json_backend.record_call(
                "function", Record(args=(9,), kwargs={"b": 11}, result=20)
            )
            assert json_backend.get_result("function", 3, b=4) == 7
            assert json_backend.get_result("function", 9, b=11) == 20

    def test_json_backend_no_value(self):
        with tempfile.NamedTemporaryFile() as temp:
            json_backend = JSONBackend(temp.name)
            with pytest.raises(RecordNotFound):
                assert json_backend.get_result("function", 3, b=4) == 7


class TestPickleBackend:
    def test_pickle_backend_get(self):
        with tempfile.NamedTemporaryFile() as temp:
            pickle_backend = PickleBackend(temp.name)
            pickle_backend.record_call(
                "function", Record(args=(3,), kwargs={"b": 4}, result=7)
            )

            new_pickle_backend = PickleBackend(temp.name)
            assert new_pickle_backend.get_result("function", 3, b=4) == 7

    def test_pickle_backend_get_multi(self):
        with tempfile.NamedTemporaryFile() as temp:
            pickle_backend = PickleBackend(temp.name)
            pickle_backend.record_call(
                "function", Record(args=(3,), kwargs={"b": 4}, result=7)
            )
            pickle_backend.record_call(
                "function", Record(args=(9,), kwargs={"b": 11}, result=20)
            )

            new_pickle_backend = PickleBackend(temp.name)
            assert new_pickle_backend.get_result("function", 3, b=4) == 7
            assert new_pickle_backend.get_result("function", 9, b=11) == 20

    def test_pickle_backend_no_value(self):
        with tempfile.NamedTemporaryFile() as temp:
            pickle_backend = PickleBackend(temp.name)
            with pytest.raises(RecordNotFound):
                assert pickle_backend.get_result("function", 3, b=4) == 7
