from collections import namedtuple

import pytest

from inspector import Inspector, Mode

Functions = namedtuple(
    "Functions", ["simplest_func", "constant_func", "args_func", "args_kwargs_func"]
)


def functions_factory(inspector: Inspector) -> Functions:
    @inspector("simplest_func")
    def simplest_func():
        return None

    @inspector("constant_func")
    def constant_func():
        return 1

    @inspector("args_func")
    def args_func(a, b):
        return a + b

    @inspector("args_kwargs_func")
    def args_kwargs_func(a, b):
        return a + b

    return Functions(simplest_func, constant_func, args_func, args_kwargs_func)


@pytest.fixture(scope="function", name="inspector")
def fixture_inspector():
    return Inspector(Mode.RECORD)


@pytest.fixture(name="simplest_func")
def fixture_simplest_func(inspector):
    functions = functions_factory(inspector)
    return functions.simplest_func


@pytest.fixture(name="constant_func")
def fixture_constant_func(inspector):
    functions = functions_factory(inspector)
    return functions.constant_func


@pytest.fixture(name="args_func")
def fixture_args_func(inspector):
    functions = functions_factory(inspector)
    return functions.args_func


@pytest.fixture(name="args_kwargs_func")
def fixture_args_kwargs_func(inspector):
    functions = functions_factory(inspector)
    return functions.args_kwargs_func
