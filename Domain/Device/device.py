from dataclasses import dataclass
from utility.exception import DeviceException
from typing import Tuple


@dataclass(frozen=True)
class DeviceID:
    id: str

    def __post_init__(self):
        if not self.id:
            raise DeviceException("idが空です")

    def get(self):
        return self.id


@dataclass(frozen=True)
class DeviceIDCollection:
    ids: Tuple[DeviceID, ...]

    def __post_init__(self):
        if not self.ids:
            raise DeviceException("idsが空です")

    def __iter__(self):
        return iter(self.ids)


# TODO ルールを内包させる
@dataclass(frozen=True)
class Device:
    id: DeviceID
    name: str
    type: str
