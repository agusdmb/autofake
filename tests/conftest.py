import pytest

from fakeit import FakeIt, Mode


@pytest.fixture(scope="function", name="fakeit")
def fixture_fakeit():
    return FakeIt(Mode.RECORD)


@pytest.fixture(name="function")
def fixture_function(fakeit):
    @fakeit("function")
    def function(a, b):
        return a + b

    return function
