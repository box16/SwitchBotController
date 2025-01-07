from dataclasses import dataclass
from utility.exception import GroupException
from Domain.Device.device import DeviceID
from typing import Tuple


@dataclass(frozen=True)
class GroupName:
    name: str

    def __post_init__(self):
        if not self.name:
            raise GroupException("nameが空です")
        if not isinstance(self.name, str):
            raise GroupException("group_nameはstrで指定してください")

    def get(self):
        return self.name


@dataclass(frozen=True)
class GroupID:
    id: int

    def __post_init__(self):
        if not self.id:
            raise GroupException("idが空です")

        if not isinstance(self.id, int):
            raise GroupException("group_idはintで指定してください")

    def get(self) -> int:
        return self.id


@dataclass(frozen=True)
class NewGroup:
    name: GroupName
    device_ids: Tuple[DeviceID, ...]


@dataclass(frozen=True)
class Group:
    id: GroupID
    name: GroupName
