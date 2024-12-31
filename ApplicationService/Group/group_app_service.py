from utility.exception import DeviceException, GroupException, CreateGroupError
from typing import Tuple
from Domain.Group.group_repository import IGroupRepository
from Domain.api_gateway import ISwitchBotGateway
from Domain.Group.group import Group, NewGroup, GroupName
from Domain.Device.device import DeviceID, DeviceIDCollection
from ApplicationService.Group.group_dto import Group as DGroup
from ApplicationService.Group.group_command import CreateGroupCommand


class GroupAppService:
    def __init__(
        self, group_repository: IGroupRepository, api_gateway: ISwitchBotGateway
    ):
        self.group_repository = group_repository
        self.api_gateway = api_gateway

    def create_group(self, command: CreateGroupCommand):
        try:
            device_ids = tuple(DeviceID(id) for id in command.device_list)
            new_group = NewGroup(
                GroupName(command.name), DeviceIDCollection(device_ids)
            )
            self.group_repository.add(new_group)
        except DeviceException as e:
            raise CreateGroupError(str(e))
        except GroupException as e:
            raise CreateGroupError(str(e))

    def get_all(self) -> Tuple[DGroup]:
        groups: Tuple[Group] = self.group_repository.get_all()
        return tuple(DGroup(g.id, g.name) for g in groups)
