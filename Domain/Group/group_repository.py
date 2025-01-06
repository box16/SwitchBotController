from abc import ABC, abstractmethod
from typing import Tuple
from Domain.Group.group import Group, NewGroup, GroupID
from Domain.Device.device import Device


class IGroupRepository(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Group]:
        pass

    @abstractmethod
    def add(self, new_group: NewGroup) -> None:
        pass

    @abstractmethod
    def get_devices(self, group_id: GroupID) -> Tuple[Device]:
        pass
