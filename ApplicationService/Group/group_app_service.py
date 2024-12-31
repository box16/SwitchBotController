from utility.exception import DeviceNotFound, CreateGroupError
from typing import List, Tuple
from Domain.Group.group_repository import IGroupRepository
from Domain.api_gateway import ISwitchBotGateway
from Domain.Group.group_repository import GroupCreateCommand
from Domain.Group.group import Group
from ApplicationService.Group.dto_group import Group as DGroup


class GroupAppService:
    def __init__(
        self, group_repository: IGroupRepository, api_gateway: ISwitchBotGateway
    ):
        self.group_repository = group_repository
        self.api_gateway = api_gateway

    def create_group(self, device_id_list: List[str], name: str):
        try:
            command = GroupCreateCommand(name, device_id_list)
            self.group_repository.add(command)
        except DeviceNotFound as e:
            raise e
        except CreateGroupError as e:
            raise e

    def get_all(self) -> Tuple[DGroup]:
        groups: Tuple[Group] = self.group_repository.get_all()
        return tuple(DGroup(g.id, g.name) for g in groups)
