# FakeIt

## A Python Library for Mocking Functions in Testing

FakeIt is a Python library that provides an easy way to mock functions in your
tests. It allows you to run your code normally, recording the calls and returns
for some functions, then stores the results in a backend. During testing, you
can then reproduce the results of those functions instead of running the
actual implementation. This is useful when you want to isolate the code you
are testing and avoid external dependencies, such as network calls or heavy
computations.

## Getting Started

### Installation

To install FakeIt, simply run:

```bash
pip install fakeit
```

### Initializing FakeIt

FakeIt can be initialized with a mode and a backend:

```python
from fakeit.fakeit import FakeIt, Mode
from fakeit.backend import InMemoryBackend

fakeit = FakeIt(mode=Mode.RECORD, backend=InMemoryBackend())
```

The mode can be set to Mode.PRODUCTION, Mode.FAKE, or Mode.RECORD.

## How to use FakeIt

To use FakeIt, you have to wrap the functions that have external dependencies
with a FakeIt decorator. This decorator accepts a name, which is used to store
the results of the function call with the given name.

Here's an example:

```python
from fakeit import FakeIt

fake = FakeIt(mode=FakeIt.Mode.RECORD)

@fake("get_data")
def get_data():
    return requests.get("https://www.example.com/data").json()
```

You can run your code in three modes:

In Mode.PRODUCTION, the function will be executed normally.

In Mode.FAKE, the function will return the recorded result instead of executing the implementation.

In Mode.RECORD, the function will be executed and the result will be recorded in the backend.

## Backend

FakeIt has two built-in backends: InMemoryBackend and JSONBackend. The first
one is an in-memory backend, this one is mainly used for trying out stuff, it
stores the results of function calls in memory. The second one is a JSON
backend, it stores the results of function calls in a JSON file.

Implementing new backends is pretty straight forward, so you could store the
results in a DB or anywhere really.

Here's an example of how to use the JSONBackend:

```python
from fakeit import FakeIt

fake = FakeIt(mode=FakeIt.Mode.RECORD, backend=FakeIt.JSONBackend("results.json"))

@fake("get_data")
def get_data():
    return requests.get("https://www.example.com/data").json()
```

## Why use FakeIt
FakeIt helps to isolate your code from external dependencies, making it easy to
test and debug your code. It also helps to reduce the cost of network requests
and database calls during development and testing.

## Conclusion
FakeIt is a simple, yet powerful library for managing your code's dependencies.
It helps to isolate your code from external dependencies, making it easy to
test and debug your code.

## Contributing
To contribute to FakeIt, simply fork the repository and create a pull request
with your changes.

## License
FakeIt is licensed under the MIT License. See the LICENSE file for more
information.
