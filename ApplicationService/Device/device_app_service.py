from Domain.Device.device_repository import IDeviceRepository
from Domain.Device.device import Device, DeviceID, DeviceName
from typing import Tuple, Union
from utility.exception import DeviceNotFound
from dataclasses import dataclass


@dataclass(frozen=True)
class DtODevice:
    id: str
    name: str
    type: str


class DeviceAppService:
    def __init__(self, device_repository: IDeviceRepository):
        self.device_repository = device_repository

    def get_all(self) -> Tuple[DtODevice]:
        devices: Tuple[Device] = self.device_repository.get_all()
        return tuple(DtODevice(d.id.get(), d.name.get(), d.type.name) for d in devices)

    def change_name(self, _device_id: Union[int, str], new_name: str):
        # TODO :  これはリポジトリ側に持っていける
        device_id = DeviceID(_device_id)
        if not self.device_repository.is_exist(device_id):
            raise DeviceNotFound()

        # TODO : ドメイン介さないのがいいのか検討
        self.device_repository.change_name(device_id, DeviceName(new_name))
