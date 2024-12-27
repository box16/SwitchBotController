from abc import ABC, abstractmethod
from Domain.device import Device
from typing import Tuple


class IDeviceReopsitory(ABC):
    @abstractmethod
    def get_all(self) -> Tuple[Device]:
        pass
