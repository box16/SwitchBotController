from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CreateGroupCommand:
    name: str
    device_ids: Tuple[str, ...]
