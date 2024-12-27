from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DeviceList:
    columns: Tuple[str, ...]
    devices: Tuple[Tuple[str, ...]]
