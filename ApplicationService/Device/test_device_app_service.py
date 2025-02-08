import unittest
from Domain.Device.light import Color, Brightness
from Domain.Device.device import DeviceID
from ApplicationService.Device.device_app_service import DeviceAppService
from Infra.api_gateway import FakeSwitchBotGateway
from Infra.device_repository import DeviceRepository
from utility.exception import DeviceNotFound
import os

ID = 1


class TestDeviceAppService(unittest.TestCase):
    def setUp(self):
        self.device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        self.api_gateway = FakeSwitchBotGateway()
        self.device_app_service = DeviceAppService(
            self.device_repository, self.api_gateway
        )

        self.device_repository.add(DeviceID(ID), "ColorLight", "Color Bulb")

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_happy_pass(self):
        # TODO : Lightのみ出力をfactory側で持たせているので暫定
        devices = self.device_app_service.get_all()
        self.assertEqual(len(devices), 1)

        devices = self.device_app_service.get_by_type("light")
        self.assertEqual(len(devices), 1)

        new_name = "test_light"
        self.device_app_service.change_name(ID, new_name)
        # TODO : id指定の取得が無いので暫定
        device = self.device_app_service.get_by_type("light")[0]
        self.assertEqual(device.name, new_name)


if __name__ == "__main__":
    unittest.main()
