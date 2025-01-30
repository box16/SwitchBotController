from abc import ABC, abstractmethod
from Domain.Device.device import DeviceID
from Domain.Device.light import Color, ColorTemperature, Brightness


class ISwitchBotGateway(ABC):
    @abstractmethod
    def send_toggle_switch(self, device_id: DeviceID):
        pass

    @abstractmethod
    def send_color_adjustment(self, device_id: DeviceID, color: Color):
        pass

    @abstractmethod
    def send_white_control(
        self, device_id: DeviceID, brightness: Brightness, color_temp: ColorTemperature
    ):
        pass
