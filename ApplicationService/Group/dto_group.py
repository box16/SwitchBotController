from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Group:
    id: str
    name: str
