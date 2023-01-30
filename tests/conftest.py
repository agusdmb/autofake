import pytest

from inspector import Inspector, Mode


@pytest.fixture(scope="function", name="inspector")
def fixture_inspector():
    return Inspector(Mode.RECORD)


@pytest.fixture(name="function")
def fixture_function(inspector):
    @inspector("function")
    def function(a, b):
        return a + b

    return function
