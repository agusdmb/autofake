__version__ = "0.4.0"

from .backend import JSONBackend, PickleBackend
from .exceptions import FakeItException, NotUniqueName, RecordNotFound
from .fakeit import FakeIt
from .models import Mode, Record
