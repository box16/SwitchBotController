from Domain.Device.device_repository import IDeviceRepository
from Domain.Device.device import Device
from Domain.api_gateway import ISwitchBotGateway
from ApplicationService.Device.device_dto import Device as DDevice
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
        return tuple(DDevice(d.id, d.name, d.type) for d in devices)

    def toggle_switch(self, device_id):
        if not self.device_repository.is_exist(device_id):
            raise DeviceNotFound()

        self.api_gateway.send_toggle_switch(device_id)
