from inspector import Inspector, Record, __version__


def test_version():
    assert __version__ == "0.1.0"


def test_simplest_case(simplest_func):
    assert simplest_func() is None


def test_constant_case(constant_func):
    assert constant_func() == 1


def test_args(args_func):
    assert args_func(3, 4) == 7


def test_args_and_kwargs(args_kwargs_func):
    assert args_kwargs_func(3, b=4) == 7


def test_record_simple_case(inspector: Inspector, simplest_func):
    simplest_func()
    assert inspector.get_records_of("simplest_func") == [Record()]


def test_record_constant_case(inspector: Inspector, constant_func):
    constant_func()
    assert inspector.get_records_of("constant_func") == [Record(result=1)]


def test_record_args(inspector, args_func):
    args_func(3, 4)
    assert inspector.get_records_of("args_func") == [Record(args=[3, 4], result=7)]


def test_record_args_and_kwargs(inspector: Inspector, args_kwargs_func):
    args_kwargs_func(3, b=4)
    assert inspector.get_records_of("args_kwargs_func") == [
        Record(args=[3], kwargs={"b": 4}, result=7)
    ]


def test_multiple_function_records(inspector: Inspector, constant_func, args_func):
    constant_func()
    args_func(3, 4)
    assert inspector.get_records_of("constant_func") == [Record(result=1)]
    assert inspector.get_records_of("args_func") == [Record(args=[3, 4], result=7)]


# def test_get_function_hash(inspector):
#     def function():
#         pass
#
#     assert inspector._get_hash_for(function) == ""


# record mode
# fake mode
# prod mode
