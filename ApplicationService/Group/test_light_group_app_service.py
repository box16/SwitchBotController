import unittest
import os
from Domain.Device.device import DeviceID
from ApplicationService.Group.light_group_app_service import (
    LightGroupAppService,
    CreateGroupCommand,
    UpdateGroupCommand,
)
from Infra.device_repository import DeviceRepository
from Infra.group_repository import GroupRepository
from Infra.api_gateway import FakeSwitchBotGateway


class TestLightGroupAppService(unittest.TestCase):
    def setUp(self):
        self.device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        self.group_repository = GroupRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        api_gateway = FakeSwitchBotGateway()

        self.device_repository.add(DeviceID(1), "ColorLight1", "Color Bulb")
        self.device_repository.add(DeviceID(2), "ColorLight2", "Color Bulb")
        self.device_repository.add(DeviceID(3), "ColorLight3", "Color Bulb")

        self.light_group_app_service = LightGroupAppService(
            self.group_repository, self.device_repository, api_gateway
        )

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_happy_pass(self):
        GROUP_ID = 1
        command = CreateGroupCommand("group1", ["1", "2", "3"])
        self.light_group_app_service.create_group(command)
        result = self.light_group_app_service.get_all()
        self.assertEqual(len(result), 1)

        self.device_repository.add(DeviceID(4), "ColorLight4", "Color Bulb")
        update_command = UpdateGroupCommand((4,), (1, 2))
        self.light_group_app_service.update_group(GROUP_ID, update_command)
        result = self.light_group_app_service.get_member_by_id(GROUP_ID)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
