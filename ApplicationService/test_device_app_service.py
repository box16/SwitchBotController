import unittest
from .device_app_service import DeviceAppService
from Infra.device_repository import InMemoryRepository
from Infra.api_gateway import FakeSwitchBotGateway


class TestDeviceAppService(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryRepository()
        self.api_gateway = FakeSwitchBotGateway()
        self.device_app_service = DeviceAppService(self.db, self.api_gateway)

    def test_get_all(self):
        self.db.add("1", "ColorLight", "Color Bulb")
        device_list = self.device_app_service.get_all()
        self.assertEqual(len(device_list.devices), 1)

    def test_toggle_switch(self):
        device_id = 1
        self.db.add(device_id, "ColorLight", "Color Bulb")
        response = self.device_app_service.toggle_switch(device_id)
        self.assertTrue(response)

    def test_toggle_switch_non_existent_device(self):
        device_id = 1
        self.db.add(device_id, "ColorLight", "Color Bulb")
        response = self.device_app_service.toggle_switch(device_id + 1)
        self.assertFalse(response)


if __name__ == "__main__":
    unittest.main()
