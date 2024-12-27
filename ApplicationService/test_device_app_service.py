import unittest
from .device_app_service import DeviceAppService


class TestDeviceAppService(unittest.TestCase):
    def setUp(self):
        self.device_app_service = DeviceAppService()

    def test_get(self):
        device_list = self.device_app_service.get()
        self.assertIsNotNone(device_list)


if __name__ == "__main__":
    unittest.main()
