from Domain.Device.device_repository import IDeviceRepository
from Domain.Device.device import DeviceID, DeviceType
from Domain.Device.light import Color, Brightness, ColorTemperature
from Domain.api_gateway import ISwitchBotGateway
from ApplicationService.Device.device_app_service import DtODevice
from typing import Union
from utility.exception import DeviceNotFound
from dataclasses import dataclass


@dataclass(frozen=True)
class DtOColor:
    red: int
    green: int
    blue: int


class LightAppService:
    def __init__(
        self, device_repository: IDeviceRepository, api_gateway: ISwitchBotGateway
    ):
        self.device_repository = device_repository
        self.api_gateway = api_gateway

    def get_all(self):
        devices = self.device_repository.get_by_type(DeviceType.LIGHT)
        return tuple(DtODevice(d.id.get(), d.name.get(), d.type.name) for d in devices)

    def toggle_switch(self, _device_id: Union[str, int]):
        device_id = DeviceID(_device_id)
        if not self.device_repository.is_exist(device_id):
            raise DeviceNotFound()

        self.api_gateway.send_toggle_switch(device_id)

    def white_control(
        self, _device_id: Union[str, int], _brightness: str, _color_temp: str
    ):
        # TODO : なんか無駄な気がする
        device_id = DeviceID(_device_id)
        if not self.device_repository.is_exist(device_id):
            raise DeviceNotFound()

        device = self.device_repository.get_by_id(device_id)
        if not (device.type == DeviceType.LIGHT):
            raise DeviceNotFound(f"LIGHTではありません")

        # TODO : これ受け方考えたい
        brightness = Brightness(_brightness)
        color_temp = ColorTemperature(int(_color_temp))
        self.api_gateway.send_white_control(device_id, brightness, color_temp)

    def color_control(
        self,
        _device_id: Union[str, int],
        _color: DtOColor,
        _brightness: Union[str, int],
    ):
        # TODO : なんか無駄な気がする
        device_id = DeviceID(_device_id)
        if not self.device_repository.is_exist(device_id):
            raise DeviceNotFound()

        device = self.device_repository.get_by_id(device_id)
        if not (device.type == DeviceType.LIGHT):
            raise DeviceNotFound(f"LIGHTではありません")

        color = Color(_color.red, _color.green, _color.blue)
        brightness = Brightness(_brightness)
        self.api_gateway.send_color_control(device_id, color, brightness)
