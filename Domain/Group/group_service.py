from abc import ABC, abstractmethod
from Domain.Device.device import DeviceID, Device, DeviceType
from Domain.Group.group import GroupID
from Domain.Device.device_repository import IDeviceRepository
from Domain.Group.group_repository import IGroupRepository
from typing import List
from utility.exception import CreateGroupError


class GroupService(ABC):
    @abstractmethod
    def can_create(self, ids: List[DeviceID]) -> bool:
        pass

    @abstractmethod
    def can_add_device(self, group_id: GroupID, device_ids: List[DeviceID]) -> bool:
        pass

    @abstractmethod
    def can_remove_device(self, group_id: GroupID, device_ids: List[DeviceID]) -> bool:
        pass


class LightGroupService(GroupService):
    def __init__(
        self, device_repository: IDeviceRepository, group_repository: IGroupRepository
    ):
        self.device_repository = device_repository
        self.group_repository = group_repository

    def _check_light_group_rule(self, ids: List[DeviceID]) -> bool:
        if not ids:
            return False

        for id in ids:
            if not self.device_repository.is_exist(id):
                return False

            device: Device = self.device_repository.get_by_id(id)
            if not device.type == DeviceType.LIGHT:
                return False
        return True

    def can_create(self, ids: List[DeviceID]) -> bool:
        return self._check_light_group_rule(ids)

    def can_add_device(self, group_id: GroupID, device_ids: List[DeviceID]) -> bool:
        if not self._check_light_group_rule(device_ids):
            return False

        # 追加済みならば追加しない
        now_devices = self.group_repository.get_device_ids(group_id)
        return len(set(device_ids) & set(now_devices)) == 0

    def can_remove_device(self, group_id: GroupID, device_ids: List[DeviceID]) -> bool:
        now_device_num = len(self.group_repository.get_device_ids(group_id))
        remove_device_num = len(device_ids)

        # グループは2個以上
        if (now_device_num - remove_device_num) < 2:
            return False

        for device in device_ids:
            if not self.device_repository.is_exist(device):
                return False

        return True
