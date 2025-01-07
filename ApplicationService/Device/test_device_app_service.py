import unittest
from ApplicationService.Device.device_app_service import DeviceAppService
from Infra.api_gateway import FakeSwitchBotGateway
from Infra.device_repository import DeviceRepository
from utility.exception import DeviceNotFound
import os


class TestDeviceAppService(unittest.TestCase):
    def setUp(self):
        self.db = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        self.api_gateway = FakeSwitchBotGateway()
        self.device_app_service = DeviceAppService(self.db, self.api_gateway)

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_get_all(self):
        self.db.add("1", "ColorLight", "Color Bulb")
        device_ids = self.device_app_service.get_all()
        self.assertEqual(len(device_ids), 1)

    def test_toggle_switch(self):
        device_id = 1
        self.db.add(device_id, "ColorLight", "Color Bulb")
        try:
            self.device_app_service.toggle_switch(device_id)
        except Exception as e:
            assert False, f"{e}"

    def test_toggle_switch_non_existent_device(self):
        device_id = 1
        self.db.add(device_id, "ColorLight", "Color Bulb")
        with self.assertRaises(DeviceNotFound):
            self.device_app_service.toggle_switch(device_id + 1)


if __name__ == "__main__":
    unittest.main()
