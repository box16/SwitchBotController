import unittest
import os
from Domain.Device.device import DeviceID
from Infra.device_repository import DeviceRepository
from Infra.group_repository import GroupRepository
from Domain.Group.group_service import LightGroupService
from utility.exception import DeviceException


class TestLightGroupService(unittest.TestCase):
    def setUp(self):
        self.device_repository = DeviceRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))
        self.group_repository = GroupRepository(os.getenv("SWITCHBOT_TEST_DB_PATH"))

        self.device_repository.add(DeviceID(1), "ColorLight1", "Color Bulb")
        self.device_repository.add(DeviceID(2), "ColorLight2", "Color Bulb")
        self.device_repository.add(DeviceID(3), "ColorLight3", "Color Bulb")

        self.light_group_service = LightGroupService(
            self.device_repository, self.group_repository
        )

    def tearDown(self):
        os.remove(os.getenv("SWITCHBOT_TEST_DB_PATH"))

    def test_create_group_only_light(self):
        result = self.light_group_service.can_create(
            [DeviceID(1), DeviceID(2), DeviceID(3)]
        )
        self.assertTrue(result)

    def test_create_group_with_not_light(self):
        self.device_repository.add(DeviceID(4), "Curtain", "Curtain")
        # TODO : Light以外未対応のため暫定
        with self.assertRaises(DeviceException):
            result = self.light_group_service.can_create(
                [DeviceID(1), DeviceID(2), DeviceID(3), DeviceID(4)]
            )
        # self.assertFalse(result)

    def test_create_group_no_device(self):
        result = self.light_group_service.can_create([])
        self.assertFalse(result)
