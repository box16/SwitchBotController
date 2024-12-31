from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Device:
    id: str
    name: str
    type: str
