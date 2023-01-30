from unittest import mock

from inspector import Inspector, Record, __version__
from inspector.inspector import Mode


def test_version():
    assert __version__ == "0.1.0"


def test_simplest_case(simplest_func):
    assert simplest_func() is None, "simplest_func returns None"


def test_constant_case(constant_func):
    assert constant_func() == 1, "constant_func returns 1"


def test_args(args_func):
    assert args_func(3, 4) == 7, "args_func returns correct value"


def test_args_and_kwargs(args_kwargs_func):
    assert args_kwargs_func(3, b=4) == 7, "args_kwargs_func returns correct value"


def test_record_simple_case(inspector: Inspector, simplest_func):
    simplest_func()
    assert inspector.get_records_of("simplest_func") == [
        Record()
    ], "Record simplest_func"


def test_record_constant_case(inspector: Inspector, constant_func):
    constant_func()
    assert inspector.get_records_of("constant_func") == [
        Record(result=1)
    ], "Record constant_func"


def test_record_args(inspector, args_func):
    args_func(3, 4)
    assert inspector.get_records_of("args_func") == [
        Record(args=(3, 4), result=7)
    ], "Record args_func"


def test_record_args_and_kwargs(inspector: Inspector, args_kwargs_func):
    args_kwargs_func(3, b=4)
    assert inspector.get_records_of("args_kwargs_func") == [
        Record(args=(3,), kwargs={"b": 4}, result=7)
    ], "Record args_kwargs_func"


def test_multiple_function_records(inspector: Inspector, constant_func, args_func):
    constant_func()
    args_func(3, 4)
    assert inspector.get_records_of("constant_func") == [
        Record(result=1)
    ], "Record of constant_func while call with args_func"
    assert inspector.get_records_of("args_func") == [
        Record(args=(3, 4), result=7)
    ], "Record of args_func while call with constant_func"


def test_multiple_records_function(inspector: Inspector, args_func):
    args_func(3, 4)
    args_func(6, 7)
    assert inspector.get_records_of("args_func") == [
        Record(args=(3, 4), result=7),
        Record(args=(6, 7), result=13),
    ], "Records of function called multiple times"


def test_production_does_nothing():
    inspector = Inspector(Mode.PRODUCTION)

    @inspector("function")
    def function():
        return 1

    function()

    assert not inspector.get_records_of(
        "function"
    ), "Mode Production doesn't record anything"


def test_get_recrods(inspector: Inspector, args_func, args_kwargs_func):
    args_func(3, 4)
    args_func(6, 7)
    args_kwargs_func(8, b=9)

    assert inspector.get_records() == {
        "args_func": [
            Record(args=(3, 4), kwargs={}, result=7),
            Record(args=(6, 7), kwargs={}, result=13),
        ],
        "args_kwargs_func": [Record(args=(8,), kwargs={"b": 9}, result=17)],
    }


def test_reply():
    inspector = Inspector(Mode.FAKE)
    inspector.load_records({"function": [Record((3,), {"b": 4}, result=7)]})

    @inspector("function")
    def function(a, *, b):
        raise Exception("Should not run")

    assert function(3, b=4) == 7


def test_get_record():
    inspector = Inspector(Mode.FAKE)
    records = {"first_func": [Record()], "second_func": [Record((3, 4), result=7)]}
    inspector.load_records(records)
    assert inspector._get_result_from("second_func", *(3, 4)) == 7


def test_backend_record():
    fake_backend = mock.MagicMock()
    inspector = Inspector(mode=Mode.RECORD, backend=fake_backend)

    @inspector("function")
    def function():
        return 1

    function()

    fake_backend.assert_called_once_with(inspector.get_records_of("function")[0])
