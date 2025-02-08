import unittest
import os
from Domain.Device.device import DeviceID, DeviceName, DeviceType
from Infra.device_repository import DeviceRepository
from typing import Tuple


class TestDeviceRepository(unittest.TestCase):
    def setUp(self):
        self.device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))

        self.device_repository.add(DeviceID(1), "ColorLight1", "Color Bulb")
        self.device_repository.add(DeviceID(2), "ColorLight2", "Color Bulb")
        self.device_repository.add(DeviceID(3), "ColorLight3", "Color Bulb")

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_change_name(self):
        device_id = DeviceID(1)
        new_name = DeviceName("AAA")
        device = self.device_repository.get_by_id(device_id)
        self.assertNotEqual(device.name, new_name)
        del device

        self.device_repository.change_name(device_id, new_name)
        device = self.device_repository.get_by_id(device_id)
        self.assertEqual(device.name, new_name)

    def test_get_by_type(self):
        result = self.device_repository.get_by_type(DeviceType.LIGHT)
        self.assertEqual(len(result), 3)
