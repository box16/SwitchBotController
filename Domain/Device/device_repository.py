from abc import ABC, abstractmethod
from Domain.Device.device import Device, DeviceID, DeviceName
from typing import Tuple


class IDeviceRepository(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Device]:
        pass

    @abstractmethod
    def is_exist(self, device_id: DeviceID) -> bool:
        pass

    @abstractmethod
    def add(self) -> None:
        pass

    @abstractmethod
    def get_by_id(self, device_id: DeviceID) -> Device:
        pass

    @abstractmethod
    def change_name(self, device_id: DeviceID, device_name: DeviceName) -> Device:
        pass
