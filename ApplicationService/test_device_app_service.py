import unittest
from .device_app_service import DeviceAppService
from Infra.device_repository import InMemoryRepository


class TestDeviceAppService(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryRepository()
        self.device_app_service = DeviceAppService(self.db)

    def test_get_all(self):
        self.db.add("1", "ColorLight", "Color Bulb")
        device_list = self.device_app_service.get_all()
        self.assertEqual(len(device_list.devices), 1)


if __name__ == "__main__":
    unittest.main()
