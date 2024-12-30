from Domain.group_repository import IGroupRepository
from Domain.group import Group
from typing import Tuple


class InMemoryGroupRepository(IGroupRepository):
    def get_all(self) -> Tuple[Group]:
        return None
