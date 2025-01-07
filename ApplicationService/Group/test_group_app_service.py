import unittest
import os
from utility.exception import CreateGroupError, ControlGroupError
from Domain.Group.group import GroupID, Group
from ApplicationService.Group.group_app_service import GroupAppService
from ApplicationService.Group.group_command import CreateGroupCommand
from Infra.device_repository import DeviceRepository
from Infra.group_repository import GroupRepository
from Infra.api_gateway import FakeSwitchBotGateway


class TestGroupAppService(unittest.TestCase):
    def setUp(self):
        device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        self.group_repository = GroupRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        api_gateway = FakeSwitchBotGateway()
        self.group_app_service = GroupAppService(
            self.group_repository, device_repository, api_gateway
        )

        device_repository.add("1", "ColorLight1", "Color Bulb")
        device_repository.add("2", "ColorLight2", "Color Bulb")
        device_repository.add("3", "ColorLight3", "Color Bulb")

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

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

    def test_toggle_switch_group(self):
        command = CreateGroupCommand("group1", ["1", "2", "3"])
        self.group_app_service.create_group(command)
        all_group = self.group_app_service.get_all()
        group_id = all_group[0].id
        try:
            self.group_app_service.toggle_switch(group_id)
        except Exception as e:
            assert False, f"{e}"

    def test_toggle_switch_group(self):
        command = CreateGroupCommand("group1", ["1", "2", "3"])
        self.group_app_service.create_group(command)
        all_group = self.group_app_service.get_all()
        with self.assertRaises(ControlGroupError):
            group_id = GroupID(all_group[0].id + 1)
            self.group_app_service.toggle_switch(group_id)


if __name__ == "__main__":
    unittest.main()
