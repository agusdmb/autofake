![Tests](https://github.com/agusdmb/autofake/actions/workflows/tests.yml/badge.svg)

# AutoFake

## A Python Library for Mocking Functions in Testing

 AutoFake is a Python library that makes it easy to mock functions in your
 tests. It allows you to run your code normally and records the calls and
 returns of specified functions. The results are then stored in a backend.
 During testing, you can reproduce the results of these functions instead of
 executing their actual implementation, which is useful for isolating the code
 you are testing and avoiding external dependencies, side effects, and
 long-running functions. AutoFake is also well-suited for adding tests to
 legacy code and refactoring (it works well with
 [ApprovalTesting](https://approvaltests.com/))

## Getting Started

### Installation

To install AutoFake, simply run:

```bash
pip install autofake
```

### Usage

Here's an example of how to use AutoFake:


```python
# example.py

import smtplib
import time

import requests

from autofake import FakeIt, PickleBackend

fakeit = FakeIt(backend=PickleBackend("output.pickle"))


# Mocking external services
@fakeit("get_data")
def get_data(payload):
    return requests.get("https://www.example.com/data", params=payload).json()


# Avoiding side effects
@fakeit("send_email")
def send_email(to, subject, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("email@example.com", "password")
    message = f"Subject: {subject}\n\n{message}"
    server.sendmail("email@example.com", to, message)
    server.quit()


# As a cache for long running functions
@fakeit("long_running_process")
def long_running_process(duration, n):
    time.sleep(duration)
    return n

```

To record the function calls, parameters, and results, run:

```bash
AUTOFAKE=RECORD python example.py
```

This will run the functions normally and store the results in the
`output.pickle` file.

To fake the functions, run:

```bash
AUTOFAKE=FAKE python example.py
```

This time, the decorated functions will not be executed but their return values
(if any) will be retrieved from the backend.

## The FakeIt Object

The `FakeIt` class is the main class in AutoFake and can be initialized with a
mode and a backend.

### Modes

You can run your code in three modes:

- `PRODUCTION` mode: the function will be executed normally without any action
  (this is the default behavior).

- `RECORD` mode: the function will be executed normally and the call,
  arguments, and result will be recorded in the backend.

- `FAKE` mode: the function will not be executed, and its recorded result will
  be retrieved from the backend for the given arguments.

You can either set the mode when instantiating the FakeIt class by passing the
argument mode, or by setting an environment variable `AUTOFAKE` to one of
`PRODUCTION`, `RECORD` or `FAKE`.

### Backends

The backend determines where the calls, parameters and returns values are
stored. Different backends are provided such as `PickleBackend` and
`JSONBackend`. Pass the backend as an argument to the FakeIt Initialization.

### Decorating functions

To use FakeIt, you have to wrap the functions you want to fake with a FakeIt
decorator. This decorator accepts a name, which is used to store the results of
the function call with the given name.

## Contributing

To contribute to AutoFake, simply fork the repository and create a pull request
with your changes.

## License

AutoFake is licensed under the MIT License. See the LICENSE file for more
information.
