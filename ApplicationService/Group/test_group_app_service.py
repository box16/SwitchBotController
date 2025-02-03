import unittest
import os
from Domain.Device.device import DeviceID
from ApplicationService.Group.group_app_service import (
    LightGroupAppService,
    CreateGroupCommand,
    DtOGroup,
)
from Infra.device_repository import DeviceRepository
from Infra.group_repository import GroupRepository
from Infra.api_gateway import FakeSwitchBotGateway


class TestLightGroupAppService(unittest.TestCase):
    def setUp(self):
        device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        group_repository = GroupRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        api_gateway = FakeSwitchBotGateway()

        device_repository.add(DeviceID(1), "ColorLight1", "Color Bulb")
        device_repository.add(DeviceID(2), "ColorLight2", "Color Bulb")
        device_repository.add(DeviceID(3), "ColorLight3", "Color Bulb")

        self.light_group_app_service = LightGroupAppService(
            group_repository, device_repository, api_gateway
        )

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_happy_pass(self):
        command = CreateGroupCommand("group1", ["1", "2", "3"])
        self.light_group_app_service.create_group(command)
        result = self.light_group_app_service.get_all()
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
