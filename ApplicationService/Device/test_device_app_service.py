import unittest
from Domain.Device.device import DeviceID
from ApplicationService.Device.device_app_service import (
    DeviceAppService,
)
from Infra.device_repository import DeviceRepository
import os

ID = 1


class TestDeviceAppService(unittest.TestCase):
    def setUp(self):
        self.device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        self.device_app_service = DeviceAppService(self.device_repository)

        self.device_repository.add(DeviceID(ID), "ColorLight", "Color Bulb")
        self.device_repository.add(DeviceID(ID + 1), "Curtain", "Curtain")

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_happy_pass(self):
        devices = self.device_app_service.get_all()
        self.assertEqual(len(devices), 2)

        new_name = "test_light"
        self.device_app_service.change_name(ID, new_name)
        device = self.device_app_service.get_all()[0]
        self.assertEqual(device.name, new_name)


if __name__ == "__main__":
    unittest.main()
