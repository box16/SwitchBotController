from Domain.Device.device_repository import IDeviceRepository
from Domain.Device.device import Device
from typing import Tuple
import sqlite3
from contextlib import contextmanager


@contextmanager
def make_connection(db_path: str):
    connection = sqlite3.connect(db_path)
    try:
        yield connection
    except sqlite3.IntegrityError as e:
        connection.rollback()
        connection.close()
        raise e
    finally:
        connection.commit()
        connection.close()


class DeviceRepository(IDeviceRepository):
    def __init__(self, db_path):
        self.db_path = db_path
        with make_connection(self.db_path) as connection:
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

    def get_all(self) -> Tuple[Device]:
        with make_connection(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id,name,type FROM devices")
            result = cursor.fetchall()

        devices = []
        for r in result:
            device = Device(r[0], r[1], r[2])
            devices.append(device)
        return tuple(devices)

    def is_exist(self, device_id) -> bool:
        with make_connection(self.db_path) as connection:
            cursor = connection.cursor()
            # executeはパラメーターにシーケンスを要求するため、引数1つでもこのように指定する
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM devices WHERE id=?)", (device_id,)
            )
            # fetchone() は (0,) または (1,) のタプルを返すので、添字 [0] を取り出して bool にする
            is_exist = bool(cursor.fetchone()[0])
        return is_exist

    def add(self, id, name, type, enable_cloud=True, hub_device_id="0000"):
        with make_connection(self.db_path) as connection:
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
