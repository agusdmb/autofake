from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Tuple


@dataclass
class Record:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)
    result: Any = None


class Mode(Enum):
    RECORD = auto()
    FAKE = auto()
    PRODUCTION = auto()
