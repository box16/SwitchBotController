from abc import ABC, abstractmethod
from Domain.Group.group import Group
from typing import Tuple, List


class IGroupRepository(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Group]:
        pass

    @abstractmethod
    def add(self, device_id_list: List[str], name: str) -> None:
        pass
