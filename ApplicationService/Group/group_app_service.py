from utility.exception import CreateGroupError, GroupException
from Domain.Group.group_repository import IGroupRepository
from Domain.api_gateway import ISwitchBotGateway
from Domain.Group.group import NewGroup, GroupName, GroupType, GroupID
from Domain.Device.device import DeviceID
from Domain.Device.light import ColorTemperature, Color, Brightness
from ApplicationService.color_dto import Color as DtOColor
from Domain.Device.device_repository import IDeviceRepository
from Domain.Group.group_service import LightGroupService
from dataclasses import dataclass
from typing import Tuple, Union
from ApplicationService.Device.device_app_service import DtODevice


@dataclass(frozen=True)
class CreateGroupCommand:
    name: str
    device_ids: Tuple[str, ...]


@dataclass(frozen=True)
class UpdateGroupCommand:
    add_devices: Tuple[str, ...]
    remove_devices: Tuple[str, ...]


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
        self.light_group_service = LightGroupService(
            self.device_repository, self.group_repository
        )

    def get_all(self):
        groups = self.group_repository.get_by_type(GroupType.LIGHT)
        result = tuple(DtOGroup(g.id.get(), g.name.get(), g.type.name) for g in groups)
        return result

    def get_by_id(self, _id: Union[str, int]):
        id = GroupID(_id)
        if not self.group_repository.is_exist(id):
            raise GroupException("存在しないグループです")

        result = self.group_repository.get_by_id(id)
        if not result.type == GroupType.LIGHT:
            raise GroupException("LIGHTグループではありません")

        return DtOGroup(result.id.get(), result.name.get(), result.type.name)

    def get_member_by_id(self, _id: Union[str, int]):
        id = GroupID(_id)
        if not self.group_repository.is_exist(id):
            raise GroupException("存在しないグループです")

        result = self.group_repository.get_by_id(id)
        if not result.type == GroupType.LIGHT:
            raise GroupException("LIGHTグループではありません")

        device_ids = self.group_repository.get_member_by_id(id)
        devices = []
        for d_id in device_ids:
            devices.append(self.device_repository.get_by_id(d_id))

        return tuple(DtODevice(d.id.get(), d.name.get(), d.type.name) for d in devices)

    def create_group(self, command: CreateGroupCommand):
        ids = [DeviceID(id) for id in command.device_ids]
        if not self.light_group_service.can_create(ids):
            raise CreateGroupError("グループを作れません")

        new_group = NewGroup(GroupName(command.name), ids, GroupType.LIGHT)
        self.group_repository.add(new_group)

    def switch_on(self, _group_id: Union[str, int]):
        group_id = GroupID(_group_id)
        if not self.group_repository.is_exist(group_id):
            raise GroupException("存在しないグループです")

        ids = self.group_repository.get_device_ids(group_id)
        for id in ids:
            self.api_gateway.send_switch_on(id)

    def switch_off(self, _group_id: Union[str, int]):
        group_id = GroupID(_group_id)
        if not self.group_repository.is_exist(group_id):
            raise GroupException("存在しないグループです")

        ids = self.group_repository.get_device_ids(group_id)
        for id in ids:
            self.api_gateway.send_switch_off(id)

    def white_control(
        self, _group_id: Union[str, int], _brightness: str, _color_temp: str
    ):
        group_id = GroupID(_group_id)
        if not self.group_repository.is_exist(group_id):
            raise GroupException("存在しないグループです")

        brightness = Brightness(_brightness)
        color_temp = ColorTemperature(int(_color_temp))
        ids = self.group_repository.get_device_ids(group_id)
        for id in ids:
            self.api_gateway.send_white_control(id, brightness, color_temp)

    def color_control(
        self,
        _group_id: Union[str, int],
        _color: DtOColor,
        _brightness: Union[str, int],
    ):
        group_id = GroupID(_group_id)
        if not self.group_repository.is_exist(group_id):
            raise GroupException("存在しないグループです")

        brightness = Brightness(_brightness)
        color = Color(_color.red, _color.green, _color.blue)
        ids = self.group_repository.get_device_ids(group_id)
        for id in ids:
            self.api_gateway.send_color_control(id, color, brightness)

    def change_name(self, _group_id: Union[str, int], _new_name: str):
        group_id = GroupID(_group_id)
        if not self.group_repository.is_exist(group_id):
            raise GroupException("存在しないグループです")

        new_name = GroupName(_new_name)
        self.group_repository.change_name(group_id, new_name)

    def update_group(
        self, _group_id: Union[str, int], update_command: UpdateGroupCommand
    ):
        group_id = GroupID(_group_id)
        if not self.group_repository.is_exist(group_id):
            raise GroupException("存在しないグループです")

        add_devices = tuple(DeviceID(d) for d in update_command.add_devices)
        can_add = self.light_group_service.can_add_device(group_id, add_devices)
        if can_add:
            self.group_repository.add_device(group_id, add_devices)

        remove_devices = tuple(DeviceID(d) for d in update_command.remove_devices)
        can_remove = self.light_group_service.can_remove_device(
            group_id, remove_devices
        )
        if can_remove:
            self.group_repository.remove_device(group_id, remove_devices)
