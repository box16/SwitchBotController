import unittest
from Domain.color import Color
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

    def test_get_all(self):
        device_ids = self.device_app_service.get_all()
        self.assertEqual(len(device_ids), 1)

    def test_toggle_switch(self):
        try:
            self.device_app_service.toggle_switch(ID)
        except Exception as e:
            assert False, f"{e}"

    def test_toggle_switch_non_existent_device(self):
        with self.assertRaises(DeviceNotFound):
            self.device_app_service.toggle_switch(ID + 1)

    def test_color_adjustment(self):
        try:
            color = Color(100, 100, 100)
            self.device_app_service.color_adjustment(ID, color)
        except Exception as e:
            assert False, f"{e}"


if __name__ == "__main__":
    unittest.main()
