from dataclasses import dataclass
from utility.exception import GroupException
from Domain.Device.device import DeviceID
from typing import Tuple, Union
from enum import Enum


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


class GroupType(Enum):
    LIGHT = 1
    MIX = 2


@dataclass(frozen=True)
class NewGroup:
    name: GroupName
    device_ids: Tuple[DeviceID, ...]
    type: GroupType


class Group:
    def __init__(
        self,
        id: Union[GroupID, str, int],
        name: Union[GroupName, str],
        type: GroupType,
    ):
        self.id = self._to_group_id(id)
        self.name = self._to_group_name(name)
        if not type in GroupType:
            raise GroupException(f"GroupTypeで指定してください")
        self.type = type

    @staticmethod
    def _to_group_id(value):
        if isinstance(value, GroupID):
            return value
        elif isinstance(value, str):
            return GroupID(int(value))
        elif isinstance(value, int):
            return GroupID(value)
        else:
            raise GroupException(f"GroupIDかstr,intで指定してください")

    @staticmethod
    def _to_group_name(value):
        if isinstance(value, GroupName):
            return value
        elif isinstance(value, str):
            return GroupName(value)
        else:
            raise GroupException(f"GroupNameかstrで指定してください")
