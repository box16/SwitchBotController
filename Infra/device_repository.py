from Domain.device_repository import IDeviceRepository
from Domain.device import Device
from typing import Tuple
import sqlite3
import os


class DeviceRepository(IDeviceRepository):
    def __init__(self):
        self_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self_dir, "devices.db")

    def get_all(self) -> Tuple[Device]:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT id,name,type FROM devices")
        result = cursor.fetchall()
        connection.close()

        devices = []
        for r in result:
            device = Device(r[0], r[1], r[2])
            devices.append(device)

        return tuple(devices)

    def is_exist(self, device_id) -> bool:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # executeはパラメーターにシーケンスを要求するため、引数1つでもこのように指定する
        cursor.execute("SELECT EXISTS(SELECT 1 FROM devices WHERE id=?)", (device_id,))
        # fetchone() は (0,) または (1,) のタプルを返すので、添字 [0] を取り出して bool にする
        return bool(cursor.fetchone()[0])


class InMemoryRepository(IDeviceRepository):
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")
        cursor = self.connection.cursor()
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
        self.connection.commit()

    def add(self, id, name, type, enable_cloud=True, hub_device_id="0000"):
        cursor = self.connection.cursor()
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
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT id,name,type FROM devices")
        result = cursor.fetchall()

        devices = []
        for r in result:
            device = Device(r[0], r[1], r[2])
            devices.append(device)

        return tuple(devices)

    def is_exist(self, device_id) -> bool:
        cursor = self.connection.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM devices WHERE id=?)", (device_id,))
        return bool(cursor.fetchone()[0])
