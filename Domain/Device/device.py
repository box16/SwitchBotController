from dataclasses import dataclass
from utility.exception import DeviceException
from enum import Enum
from typing import Union


@dataclass(frozen=True)
class DeviceID:
    id: str

    def __post_init__(self):
        if not self.id:
            raise DeviceException("idが空です")
        object.__setattr__(self, "id", self._to_id(self.id))

    @staticmethod
    def _to_id(value):
        if isinstance(value, str):
            return value
        elif isinstance(value, int):
            return str(value)
        else:
            raise DeviceException(f"strかintで指定してください")

    def get(self):
        return self.id


@dataclass(frozen=True)
class DeviceName:
    name: str

    def __post_init__(self):
        if not self.name:
            raise DeviceException("nameが空です")
        if not isinstance(self.name, str):
            raise DeviceException("nameはstrで指定してください")

    def get(self):
        return self.name


class DeviceType(Enum):
    LIGHT = 1
    OTHER = 2


class Device:
    def __init__(
        self,
        id: Union[DeviceID, str, int],
        name: Union[DeviceName, str],
        type: DeviceType,
    ):
        self.id = self._to_device_id(id)
        self.name = self._to_device_name(name)
        if not type in DeviceType:
            raise DeviceException(f"DeviceTypeで指定してください")
        self.type = type

    @staticmethod
    def _to_device_id(value):
        if isinstance(value, DeviceID):
            return value
        elif isinstance(value, str):
            return DeviceID(value)
        elif isinstance(value, int):
            return DeviceID(str(value))
        else:
            raise DeviceException(f"DeviceIDかstrで指定してください")

    @staticmethod
    def _to_device_name(value):
        if isinstance(value, DeviceName):
            return value
        elif isinstance(value, str):
            return DeviceName(value)
        else:
            raise DeviceException(f"DeviceNameかstrで指定してください")
