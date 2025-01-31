import unittest
import os
from Domain.Device.device import DeviceID, DeviceName
from Infra.device_repository import DeviceRepository
from typing import Tuple


class TestDeviceRepository(unittest.TestCase):
    def setUp(self):
        self.device_db = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))

        self.device_db.add(DeviceID(1), "ColorLight1", "Color Bulb")
        self.device_db.add(DeviceID(2), "ColorLight2", "Color Bulb")
        self.device_db.add(DeviceID(3), "ColorLight3", "Color Bulb")

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_change_name(self):
        device_id = DeviceID(1)
        new_name = DeviceName("AAA")
        device = self.device_db.get_by_id(device_id)
        self.assertNotEqual(device.name, new_name)
        del device

        self.device_db.change_name(device_id, new_name)
        device = self.device_db.get_by_id(device_id)
        self.assertEqual(device.name, new_name)
