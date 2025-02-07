import unittest
import os
from Domain.Group.group import NewGroup, GroupName, Group, GroupType, GroupID
from Domain.Device.device import DeviceID
from Infra.device_repository import DeviceRepository
from Infra.group_repository import GroupRepository
from typing import Tuple


class TestGroupRepository(unittest.TestCase):
    def setUp(self):
        self.device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        self.group_repository = GroupRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))

        self.device_repository.add(DeviceID(1), "ColorLight1", "Color Bulb")
        self.device_repository.add(DeviceID(2), "ColorLight2", "Color Bulb")
        self.device_repository.add(DeviceID(3), "ColorLight3", "Color Bulb")
        new_group = NewGroup(
            GroupName("group1"),
            tuple([DeviceID(1), DeviceID(2), DeviceID(3)]),
            GroupType.LIGHT,
        )
        self.group_repository.add(new_group)
        all_group: Tuple[Group] = self.group_repository.get_all()
        group_id = all_group[0].id
        self.INITIAL_GROUP_ID = group_id

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_get_all_one_groups(self):
        all_group = self.group_repository.get_all()
        self.assertEqual(len(all_group), 1)

    def test_get_devices(self):
        devices = self.group_repository.get_device_ids(self.INITIAL_GROUP_ID)
        self.assertEqual(len(devices), 3)

    def test_change_name(self):
        new_name = GroupName("TEST_NAME")
        old_name = self.group_repository.get_all()[0].name
        self.assertNotEqual(new_name.get(), old_name.get())

        self.group_repository.change_name(self.INITIAL_GROUP_ID, new_name)
        now_name = self.group_repository.get_all()[0].name
        self.assertEqual(new_name.get(), now_name.get())

    def test_add_device(self):
        self.device_repository.add(DeviceID(4), "ColorLight4", "Color Bulb")
        self.group_repository.add_device(self.INITIAL_GROUP_ID, (DeviceID(4),))
        devices = self.group_repository.get_device_ids(self.INITIAL_GROUP_ID)
        self.assertEqual(len(devices), 4)

    def test_remove_device(self):
        self.group_repository.remove_device(self.INITIAL_GROUP_ID, (DeviceID(1),))
        devices = self.group_repository.get_device_ids(self.INITIAL_GROUP_ID)
        self.assertEqual(len(devices), 2)

    def test_get_by_id(self):
        result = self.group_repository.get_by_id(GroupID(1))
        self.assertEqual(result.name.get(), "group1")
