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
from Domain.Device.device import DeviceID
from Domain.Device.device_repository import IDeviceRepository
from ApplicationService.Group.group_dto import Group as DGroup
from ApplicationService.Group.group_command import CreateGroupCommand


class GroupAppService:
    def __init__(
        self,
        group_repository: IGroupRepository,
        device_repository: IDeviceRepository,
        api_gateway: ISwitchBotGateway,
    ):
        self.group_repository = group_repository
        self.device_repository = device_repository
        self.api_gateway = api_gateway

    def create_group(self, command: CreateGroupCommand):
        if not command.device_ids:
            raise CreateGroupError(f"グループが空です")
        for id in command.device_ids:
            if not self.device_repository.is_exist(id):
                raise CreateGroupError(f"存在しないデバイスIDが指定されています")

        try:
            new_group = NewGroup(
                GroupName(command.name),
                tuple(DeviceID(id) for id in command.device_ids),
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
            id = GroupID(int(group_id))
            if not self.group_repository.is_exist(id):
                raise ControlGroupError(f"存在しないグループです")

            devices: Tuple[DeviceID] = self.group_repository.get_devices(id)
            for device in devices:
                self.api_gateway.send_toggle_switch(device.get())
        except GroupException as e:
            raise ControlGroupError(str(e))
