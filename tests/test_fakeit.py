import os
from typing import Callable
from unittest import mock

import pytest

from autofake import FakeIt, Mode, RecordNotFound


def test_function(function):
    assert function(3, b=4) == 7, "function works the same with decorator"


def test_production_doesnt_record():
    fake_backend = mock.MagicMock()
    fakeit = FakeIt(Mode.PRODUCTION, fake_backend)

    @fakeit
    def function():
        return 1

    function()

    fake_backend.record_call.assert_not_called()


def test_get_recrods(fakeit: FakeIt, function: Callable):
    function(3, b=4)
    function(6, b=7)

    assert fakeit._backend.get_result("function", 6, b=7) == 13
    assert fakeit._backend.get_result("function", 3, b=4) == 7


def test_get_non_existing_recrods(fakeit: FakeIt, function: Callable):
    function(3, b=4)

    with pytest.raises(RecordNotFound):
        assert fakeit._backend.get_result("function", 6, b=7) == 13


def test_replay():
    fake_backend = mock.MagicMock()
    fakeit = FakeIt(Mode.FAKE, fake_backend)

    @fakeit
    def function(a, *, b):
        raise Exception("Should not run")

    function(3, b=4)

    fake_backend.record_call.assert_not_called()
    fake_backend.get_result.assert_called_once_with("function", 3, b=4)


@pytest.mark.parametrize("mode_env", ["RECORD", "FAKE", "PRODUCTION"])
def test_env(mode_env):
    previous = os.environ.get("AUTOFAKE")
    os.environ["AUTOFAKE"] = mode_env
    fakeit = FakeIt()
    assert fakeit._mode == Mode(mode_env)
    os.environ["AUTOFAKE"] = previous or ""


@pytest.mark.parametrize("mode_env", ["RECORD", "FAKE", "PRODUCTION"])
@pytest.mark.parametrize("mode_arg", ["RECORD", "FAKE", "PRODUCTION"])
def test_env_overrited(mode_env, mode_arg):
    previous = os.environ.get("AUTOFAKE")
    os.environ["AUTOFAKE"] = mode_env
    fakeit = FakeIt(mode=Mode(mode_arg))
    assert fakeit._mode == Mode(mode_arg)
    os.environ["AUTOFAKE"] = previous or ""


def test_default_mode():
    previous = os.environ.get("AUTOFAKE")
    os.environ["AUTOFAKE"] = ""
    fakeit = FakeIt()
    assert fakeit._mode == Mode.PRODUCTION
    os.environ["AUTOFAKE"] = previous or ""
