__version__ = "0.1.0"

from .backend import JsonBackend
from .exceptions import FakeItException, RecordNotFound
from .fakeit import FakeIt
from .models import Mode, Record
