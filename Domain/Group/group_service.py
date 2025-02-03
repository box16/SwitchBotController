from abc import ABC, abstractmethod
from Domain.Device.device import DeviceID, Device, DeviceType
from Domain.Device.device_repository import IDeviceRepository
from typing import List
from utility.exception import CreateGroupError


class GroupService(ABC):
    def __init__(self, device_repository: IDeviceRepository):
        self.device_repository = device_repository

    @abstractmethod
    def can_create(self, ids: List[DeviceID]):
        pass


class LightGroupService(GroupService):
    def can_create(self, ids: List[DeviceID]) -> bool:
        if not ids:
            return False

        for id in ids:
            if not self.device_repository.is_exist(id):
                return False

            device: Device = self.device_repository.get_by_id(id)
            if not device.type == DeviceType.LIGHT:
                return False
        return True
