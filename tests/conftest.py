import pytest

from inspector import Inspector


@pytest.fixture(scope="function", name="inspector")
def fixture_inspector():
    return Inspector()


@pytest.fixture(name="simplest_func")
def fixture_simplest_func(inspector):
    @inspector("simplest_func")
    def function():
        pass

    return function


@pytest.fixture(name="constant_func")
def fixture_constant_func(inspector):
    @inspector("constant_func")
    def function():
        return 1

    return function


@pytest.fixture(name="args_func")
def fixture_args_func(inspector):
    @inspector("args_func")
    def function(a, b):
        return a + b

    return function


@pytest.fixture(name="args_kwargs_func")
def fixture_args_kwargs_func(inspector):
    @inspector("args_kwargs_func")
    def function(a, b):
        return a + b

    return function
