from typing import Callable
from unittest import mock

import pytest

from inspector import Inspector, Record, __version__
from inspector.inspector import Mode


def test_version():
    assert __version__ == "0.1.0"


def test_function(function):
    assert function(3, b=4) == 7, "function works the same with decorator"


def test_production_doesnt_record():
    fake_backend = mock.MagicMock()
    inspector = Inspector(Mode.PRODUCTION, fake_backend)

    @inspector("function")
    def function():
        return 1

    function()

    fake_backend.assert_not_called()


def test_get_recrods(inspector: Inspector, function: Callable):
    function(3, b=4)
    function(6, b=7)

    assert inspector.get_result("function", 6, b=7) == 13
    assert inspector.get_result("function", 3, b=4) == 7


def test_get_non_existing_recrods(inspector: Inspector, function: Callable):
    function(3, b=4)

    with pytest.raises(ValueError):
        assert inspector.get_result("function", 6, b=7) == 13


def test_replay():
    fake_backend = mock.MagicMock()
    inspector = Inspector(Mode.FAKE, fake_backend)

    @inspector("function")
    def function(a, *, b):
        raise Exception("Should not run")

    function(3, b=4)

    fake_backend.record_call.assert_not_called()
    fake_backend.get_result.assert_called_once_with("function", 3, b=4)
