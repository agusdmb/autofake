from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Tuple


@dataclass
class Record:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)
    result: Any = None


class Mode(str, Enum):
    RECORD = "RECORD"
    FAKE = "FAKE"
    PRODUCTION = "PRODUCTION"
