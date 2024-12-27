from abc import ABC, abstractmethod
from Domain.device import Device
from typing import Tuple


class IDeviceRepository(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Device]:
        pass
