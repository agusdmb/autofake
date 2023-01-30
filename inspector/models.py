from dataclasses import dataclass, field
from typing import Any, Tuple


@dataclass
class Record:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)
    result: Any = None
