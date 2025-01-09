from dataclasses import dataclass
from utility.exception import DeviceException


@dataclass(frozen=True)
class DeviceID:
    id: str

    def __post_init__(self):
        if not self.id:
            raise DeviceException("idが空です")

    def get(self):
        return self.id


@dataclass(frozen=True)
class Device:
    id: DeviceID
    name: str
    type: str
