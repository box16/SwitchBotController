from Domain.Device.device import Device, DeviceID, DeviceName, DeviceType
from typing import Union


class Light(Device):
    def __init__(
        self,
        id: Union[DeviceID, str, int],
        name: Union[DeviceName, str],
    ):
        super().__init__(id, name, DeviceType.LIGHT)
