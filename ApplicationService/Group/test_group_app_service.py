import unittest
from ApplicationService.Group.group_app_service import GroupAppService
from Infra.group_repository import InMemoryGroupRepository
from Infra.device_repository import InMemoryDeviceRepository
from Infra.api_gateway import FakeSwitchBotGateway


class TestGroupAppService(unittest.TestCase):
    def setUp(self):
        self.device_db = InMemoryDeviceRepository()
        self.group_db = InMemoryGroupRepository()
        self.api_gateway = FakeSwitchBotGateway()
        self.group_app_service = GroupAppService(self.group_db, self.api_gateway)

    def test_create_group(self):
        self.device_db.add("1", "ColorLight1", "Color Bulb")
        self.device_db.add("2", "ColorLight2", "Color Bulb")
        self.device_db.add("3", "ColorLight3", "Color Bulb")

        all_group = self.group_db.get_all()
        self.assertEqual(len(all_group), 0)

        self.group_app_service.create_group(["1", "2", "3"])
        all_group = self.group_db.get_all()
        self.assertEqual(len(all_group), 1)


if __name__ == "__main__":
    unittest.main()
