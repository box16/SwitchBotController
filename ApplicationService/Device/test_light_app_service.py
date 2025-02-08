import unittest
from Domain.Device.device import DeviceID
from ApplicationService.Device.light_app_service import LightAppService
from Infra.device_repository import DeviceRepository
from Infra.api_gateway import FakeSwitchBotGateway
import os

ID = 1


class TestLightAppService(unittest.TestCase):
    def setUp(self):
        self.device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        self.api_gateway = FakeSwitchBotGateway()
        self.light_app_service = LightAppService(
            self.device_repository, self.api_gateway
        )

        self.device_repository.add(DeviceID(ID), "ColorLight", "Color Bulb")
        self.device_repository.add(DeviceID(ID + 1), "Curtain", "Curtain")

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_happy_pass(self):
        devices = self.light_app_service.get_all()
        self.assertEqual(len(devices), 1)


if __name__ == "__main__":
    unittest.main()
