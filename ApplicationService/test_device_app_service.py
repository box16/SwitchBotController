import unittest
from .device_app_service import DeviceAppService
from Infra.device_repository import DeviceRepository


class TestDeviceAppService(unittest.TestCase):
    def setUp(self):
        self.device_app_service = DeviceAppService(DeviceRepository())

    def test_get_all(self):
        device_list = self.device_app_service.get_all()
        self.assertIsNotNone(device_list)


if __name__ == "__main__":
    unittest.main()
