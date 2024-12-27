from .dto_device import Device, DeviceList


class DeviceAppService:
    def __init__(self):
        pass

    def get_all(self):
        # リポジトリから全デバイス取得
        devices = []
        dto_devices = []
        for device in devices:
            dto_device = Device(device.id, device.name, device.type)
            dto_devices.append(dto_device)
        return DeviceList(("id", "name", "type"), dto_devices)
