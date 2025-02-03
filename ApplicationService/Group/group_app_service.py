from utility.exception import (
    CreateGroupError,
)
from Domain.Group.group_repository import IGroupRepository
from Domain.api_gateway import ISwitchBotGateway
from Domain.Group.group import NewGroup, GroupName, GroupType, GroupID
from Domain.Device.device import DeviceID
from Domain.Device.device_repository import IDeviceRepository
from Domain.Group.group_service import LightGroupService
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CreateGroupCommand:
    name: str
    device_ids: Tuple[str, ...]


@dataclass(frozen=True)
class DtOGroup:
    id: GroupID
    name: GroupName
    type: GroupType


class LightGroupAppService:
    def __init__(
        self,
        group_repository: IGroupRepository,
        device_repository: IDeviceRepository,
        api_gateway: ISwitchBotGateway,
    ):
        self.group_repository = group_repository
        self.device_repository = device_repository
        self.api_gateway = api_gateway

    def get_all(self):
        groups = self.group_repository.get_by_type(GroupType.LIGHT)
        result = tuple(DtOGroup(g.id.get(), g.name.get(), g.type.name) for g in groups)
        return result

    def create_group(self, command: CreateGroupCommand):
        light_group_service = LightGroupService(self.device_repository)
        ids = [DeviceID(id) for id in command.device_ids]
        if not light_group_service.can_create(ids):
            raise CreateGroupError("グループを作れません")

        new_group = NewGroup(GroupName(command.name), ids, GroupType.LIGHT)
        self.group_repository.add(new_group)
