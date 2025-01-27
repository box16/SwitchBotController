from abc import ABC, abstractmethod
from Domain.Device.device import DeviceID
from Domain.Device.light import Color


class ISwitchBotGateway(ABC):
    @abstractmethod
    def send_toggle_switch(self, device_id: DeviceID):
        pass

    @abstractmethod
    def send_color_adjustment(self, device_id: DeviceID, color: Color):
        pass
