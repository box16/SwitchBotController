import unittest
import os
from Domain.Device.device import DeviceID
from ApplicationService.Group.group_app_service import GroupAppService
from ApplicationService.Group.light_group_app_service import (
    LightGroupAppService,
    CreateGroupCommand,
)
from Infra.device_repository import DeviceRepository
from Infra.group_repository import GroupRepository
from Infra.api_gateway import FakeSwitchBotGateway


class TestGroupAppService(unittest.TestCase):
    def setUp(self):
        self.device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        self.group_repository = GroupRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        api_gateway = FakeSwitchBotGateway()

        self.device_repository.add(DeviceID(1), "ColorLight1", "Color Bulb")
        self.device_repository.add(DeviceID(2), "ColorLight2", "Color Bulb")
        self.device_repository.add(DeviceID(3), "ColorLight3", "Color Bulb")

        self.group_app_service = GroupAppService(
            self.group_repository, self.device_repository
        )

        light_group_app_service = LightGroupAppService(
            self.group_repository, self.device_repository, api_gateway
        )
        command = CreateGroupCommand("group1", ["1", "2", "3"])
        light_group_app_service.create_group(command)

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_happy_pass(self):
        GROUP_ID = 1
        result = self.group_app_service.get_all()
        self.assertEqual(len(result), 1)

        new_name = "test_name"
        self.group_app_service.change_name(GROUP_ID, new_name)
        result = self.group_app_service.get_all()[0]
        self.assertEqual(new_name, result.name)

        self.group_app_service.delete_group(GROUP_ID)
        result = self.group_app_service.get_all()
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
