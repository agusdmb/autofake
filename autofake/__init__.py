__version__ = "0.2.0"

from .backend import JSONBackend
from .exceptions import FakeItException, RecordNotFound
from .fakeit import FakeIt
from .models import Mode, Record
