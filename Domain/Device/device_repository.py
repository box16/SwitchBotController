from abc import ABC, abstractmethod
from Domain.Device.device import Device, DeviceID
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
