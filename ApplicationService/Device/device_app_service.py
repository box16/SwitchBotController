from Domain.Device.device_repository import IDeviceRepository
from Domain.Device.device import Device, DeviceID
from Domain.Device.light import Color
from Domain.api_gateway import ISwitchBotGateway
from ApplicationService.Device.device_dto import Device as DDevice
from ApplicationService.color_dto import Color as DColor
from typing import Tuple
from utility.exception import DeviceNotFound


class DeviceAppService:
    def __init__(
        self, device_repository: IDeviceRepository, api_gateway: ISwitchBotGateway
    ):
        self.device_repository = device_repository
        self.api_gateway = api_gateway

    def get_all(self) -> Tuple[DDevice]:
        devices: Tuple[Device] = self.device_repository.get_all()
        return tuple(DDevice(d.id.get(), d.name.get(), d.type.name) for d in devices)

    def toggle_switch(self, _device_id: str):
        device_id = DeviceID(_device_id)
        if not self.device_repository.is_exist(device_id):
            raise DeviceNotFound()

        self.api_gateway.send_toggle_switch(device_id)

    def color_adjustment(self, _device_id: int, d_color: DColor):
        device_id = DeviceID(_device_id)
        if not self.device_repository.is_exist(device_id):
            raise DeviceNotFound()
        color = Color(d_color.red, d_color.green, d_color.blue)
        self.api_gateway.send_color_adjustment(device_id, color)
