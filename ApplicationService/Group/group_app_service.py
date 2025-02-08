from utility.exception import GroupException
from Domain.Group.group_repository import IGroupRepository
from Domain.Group.group import GroupName, GroupID
from Domain.Device.device_repository import IDeviceRepository
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class DtOGroup:
    id: str
    name: str
    type: str


class GroupAppService:
    def __init__(
        self, group_repository: IGroupRepository, device_repository: IDeviceRepository
    ):
        self.group_repository = group_repository
        self.device_repository = device_repository

    def get_all(self):
        groups = self.group_repository.get_all()
        result = tuple(DtOGroup(g.id.get(), g.name.get(), g.type.name) for g in groups)
        return result

    def change_name(self, _group_id: Union[str, int], _new_name: str):
        # TODO : change_nameはupdateに含めていいかも
        group_id = GroupID(_group_id)
        if not self.group_repository.is_exist(group_id):
            raise GroupException("存在しないグループです")

        new_name = GroupName(_new_name)
        self.group_repository.change_name(group_id, new_name)

    def delete_group(self, _group_id: Union[str, int]):
        group_id = GroupID(_group_id)
        if not self.group_repository.is_exist(group_id):
            raise GroupException("存在しないグループです")

        self.group_repository.delete_group(group_id)
