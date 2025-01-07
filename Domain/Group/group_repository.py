from abc import ABC, abstractmethod
from typing import Tuple
from Domain.Group.group import Group, NewGroup, GroupID
from Domain.Device.device import DeviceID


class IGroupRepository(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Group]:
        pass

    @abstractmethod
    def add(self, new_group: NewGroup) -> None:
        pass

    @abstractmethod
    def get_devices(self, group_id: GroupID) -> Tuple[DeviceID]:
        pass

    @abstractmethod
    def is_exist(self, group_id: GroupID) -> bool:
        pass
