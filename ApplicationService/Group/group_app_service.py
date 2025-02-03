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
