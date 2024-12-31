from abc import ABC, abstractmethod
from typing import Tuple
from dataclasses import dataclass
from utility.exception import CreateGroupError
from Domain.Group.group import Group


@dataclass(frozen=True)
class GroupCreateCommand:
    # TODO:適宜値オブジェクト化
    name: str
    device_list: Tuple[str, ...]

    def __post_init__(self):
        if not self.name:
            raise CreateGroupError("nameが空です")
        if not self.device_list:
            raise CreateGroupError("device_listが空です")


class IGroupRepository(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Group]:
        pass

    @abstractmethod
    def add(self, command: GroupCreateCommand) -> None:
        pass
