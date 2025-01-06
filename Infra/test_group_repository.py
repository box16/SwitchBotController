import unittest
import sqlite3
from Domain.Group.group import NewGroup, GroupName
from Domain.Device.device import DeviceIDCollection, DeviceID
from Infra.device_repository import InMemoryDeviceRepository
from Infra.group_repository import InMemoryGroupRepository


class TestGroupRepository(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        device_db = InMemoryDeviceRepository(self.connection)
        device_db.add("1", "ColorLight1", "Color Bulb")
        device_db.add("2", "ColorLight2", "Color Bulb")
        device_db.add("3", "ColorLight3", "Color Bulb")

        self.group_db = InMemoryGroupRepository(self.connection)

    def test_get_all_no_groups(self):
        all_group = self.group_db.get_all()
        self.assertEqual(len(all_group), 0)

    def test_get_all_one_groups(self):
        new_group = NewGroup(
            GroupName("group1"),
            DeviceIDCollection([DeviceID(1), DeviceID(2), DeviceID(3)]),
        )
        self.group_db.add(new_group)
        all_group = self.group_db.get_all()
        self.assertEqual(len(all_group), 1)
