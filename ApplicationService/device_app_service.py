from .dto_device import Device, DeviceList
from Domain.device_repository import IDeviceReopsitory
from Domain.device import Device
from typing import Tuple


class DeviceAppService:
    def __init__(self, device_repository: IDeviceReopsitory):
        self.device_repository = device_repository

    def get_all(self):
        devices: Tuple[Device] = self.device_repository.get_all()

        dto_devices = []
        for device in devices:
            dto_devices.append((device.id, device.name, device.type))

        return DeviceList(("id", "name", "type"), dto_devices)
