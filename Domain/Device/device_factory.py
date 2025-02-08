from Domain.Device.light import Light
from Domain.Device.device import Device, DeviceType


def create_device(id: str, name: str, type: str):
    is_light = lambda x: (x == "Color Bulb") or (x == "Strip Light")
    if is_light(type):
        return Light(id, name)

    return Device(id, name, DeviceType.OTHER)
