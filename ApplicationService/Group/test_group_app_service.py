import unittest
import sqlite3
from utility.exception import CreateGroupError
from ApplicationService.Group.group_app_service import GroupAppService
from ApplicationService.Group.group_command import CreateGroupCommand
from Infra.group_repository import InMemoryGroupRepository
from Infra.device_repository import InMemoryDeviceRepository
from Infra.api_gateway import FakeSwitchBotGateway


class TestGroupAppService(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.device_db = InMemoryDeviceRepository(self.connection)
        self.group_db = InMemoryGroupRepository(self.connection)
        self.api_gateway = FakeSwitchBotGateway()
        self.group_app_service = GroupAppService(self.group_db, self.api_gateway)

        self.device_db.add("1", "ColorLight1", "Color Bulb")
        self.device_db.add("2", "ColorLight2", "Color Bulb")
        self.device_db.add("3", "ColorLight3", "Color Bulb")

    def test_get_all_no_groups(self):
        all_group = self.group_app_service.get_all()

        self.assertEqual(len(all_group), 0)

    def test_get_all_one_groups(self):
        command = CreateGroupCommand("group1", ["1", "2", "3"])
        self.group_app_service.create_group(command)
        all_group = self.group_app_service.get_all()

        self.assertEqual(len(all_group), 1)

    def test_create_group_non_existent_device_id(self):
        with self.assertRaises(CreateGroupError):
            command = CreateGroupCommand("group1", ["1", "2", "5"])
            self.group_app_service.create_group(command)

        all_group = self.group_app_service.get_all()
        self.assertEqual(len(all_group), 0)

    def test_create_group_no_device(self):
        with self.assertRaises(CreateGroupError):
            command = CreateGroupCommand("group1", [])
            self.group_app_service.create_group(command)

        all_group = self.group_app_service.get_all()
        self.assertEqual(len(all_group), 0)

    def test_create_group_no_name(self):
        with self.assertRaises(CreateGroupError):
            command = CreateGroupCommand("", ["1", "2", "3"])
            self.group_app_service.create_group(command)

        all_group = self.group_app_service.get_all()
        self.assertEqual(len(all_group), 0)


if __name__ == "__main__":
    unittest.main()
