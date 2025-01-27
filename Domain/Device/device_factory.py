from Domain.Device.device import Device, DeviceType
from utility.exception import DeviceException


def create_device(id: str, name: str, type: str):
    is_light = lambda x: (x == "Color Bulb") or (x == "Strip Light")
    if not is_light(type):
        raise DeviceException(f"未対応デバイスです")

    return Device(id, name, DeviceType.LIGHT)
