from Domain.Device.light import Light
from utility.exception import DeviceException


def create_device(id: str, name: str, type: str):
    is_light = lambda x: (x == "Color Bulb") or (x == "Strip Light")
    if is_light(type):
        return Light(id, name)

    raise DeviceException(f"未対応デバイスです")
