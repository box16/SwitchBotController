from abc import ABC, abstractmethod
from typing import Tuple
from Domain.Group.group import Group, NewGroup


class IGroupRepository(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Group]:
        pass

    @abstractmethod
    def add(self, new_group: NewGroup) -> None:
        pass
