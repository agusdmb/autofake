__version__ = "0.3.0"

from .backend import JSONBackend, PickleBackend
from .exceptions import FakeItException, RecordNotFound
from .fakeit import FakeIt
from .models import Mode, Record
