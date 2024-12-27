import unittest
from .device_app_service import DeviceAppService
from Domain.device_repository import IDeviceRepository
from Domain.device import Device
import sqlite3


class InMemoryRepository(IDeviceRepository):
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        cursor = self.conn.cursor()
        cursor.execute(
            """
                CREATE TABLE devices (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    enable_cloud_service BOOLEAN NOT NULL,
                    hub_device_id TEXT NOT NULL
                )
            """
        )
        self.conn.commit()

    def add(self, id, name, type, enable_cloud=True, hub_device_id="0000"):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO devices (id, name, type, enable_cloud_service, hub_device_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                id,
                name,
                type,
                enable_cloud,
                hub_device_id,
            ),
        )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.cursor()

        cursor.execute("SELECT id,name,type FROM devices")
        result = cursor.fetchall()

        devices = []
        for r in result:
            device = Device(r[0], r[1], r[2])
            devices.append(device)

        return tuple(devices)


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
