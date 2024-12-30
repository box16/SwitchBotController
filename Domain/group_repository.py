from abc import ABC, abstractmethod
from Domain.group import Group
from typing import Tuple


class IGroupRepository(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Group]:
        pass
