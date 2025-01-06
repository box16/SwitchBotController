from utility.exception import (
    DeviceException,
    GroupException,
    CreateGroupError,
    ControlGroupError,
)
from typing import Tuple
from Domain.Group.group_repository import IGroupRepository
from Domain.api_gateway import ISwitchBotGateway
from Domain.Group.group import Group, NewGroup, GroupName, GroupID
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
        return tuple(DGroup(g.id.get(), g.name.get()) for g in groups)

    def toggle_switch(self, group_id):
        try:
            # TODO : 問い合わせをここに持ってくる?
            devices: Tuple[DeviceID] = self.group_repository.get_devices(
                GroupID(group_id)
            )
            for device in devices:
                self.api_gateway.send_toggle_switch(device.get())
        except GroupException as e:
            raise ControlGroupError(str(e))
