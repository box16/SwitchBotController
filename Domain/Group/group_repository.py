from abc import ABC, abstractmethod
from typing import Tuple
from Domain.Group.group import Group, NewGroup, GroupID, GroupType, GroupName
from Domain.Device.device import DeviceID


class IGroupRepository(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Group]:
        pass

    @abstractmethod
    def add(self, new_group: NewGroup) -> None:
        pass

    @abstractmethod
    def get_device_ids(self, group_id: GroupID) -> Tuple[DeviceID]:
        pass

    @abstractmethod
    def is_exist(self, group_id: GroupID) -> bool:
        pass

    @abstractmethod
    def get_by_type(self, type: GroupType) -> Tuple[Group]:
        pass

    @abstractmethod
    def change_name(self, id: GroupID, new_name: GroupName):
        pass

    @abstractmethod
    def add_device(self, id: GroupID, new_devices: tuple[DeviceID]):
        pass

    @abstractmethod
    def remove_device(self, id: GroupID, remove_devices: tuple[DeviceID]):
        pass
