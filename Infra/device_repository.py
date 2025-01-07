from Domain.Device.device_repository import IDeviceRepository
from Domain.Device.device import Device
from typing import Tuple
import sqlite3


class DeviceRepository(IDeviceRepository):
    def __init__(self, db_path):
        self.db_path = db_path
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS devices (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    enable_cloud_service BOOLEAN NOT NULL,
                    hub_device_id TEXT NOT NULL
                )
            """
        )
        connection.commit()
        connection.close()

    def get_all(self) -> Tuple[Device]:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id,name,type FROM devices")
        result = cursor.fetchall()

        devices = []
        for r in result:
            device = Device(r[0], r[1], r[2])
            devices.append(device)
        connection.commit()
        connection.close()
        return tuple(devices)

    def is_exist(self, device_id) -> bool:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        # executeはパラメーターにシーケンスを要求するため、引数1つでもこのように指定する
        cursor.execute("SELECT EXISTS(SELECT 1 FROM devices WHERE id=?)", (device_id,))
        # fetchone() は (0,) または (1,) のタプルを返すので、添字 [0] を取り出して bool にする
        is_exist = bool(cursor.fetchone()[0])
        connection.commit()
        connection.close()
        return is_exist

    def add(self, id, name, type, enable_cloud=True, hub_device_id="0000"):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
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
        connection.commit()
        connection.close()
