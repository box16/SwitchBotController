from Domain.Device.device_repository import IDeviceRepository
from Domain.Device.device import Device, DeviceID
from Domain.Device.device_factory import create_device
from typing import Tuple
from Infra.repository_common import make_cursor, DEVICE_TABLE
from utility.exception import DeviceException


class DeviceRepository(IDeviceRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS {DEVICE_TABLE} (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        type TEXT NOT NULL,
                        enable_cloud_service BOOLEAN NOT NULL,
                        hub_device_id TEXT NOT NULL
                    )
                """
            )

    def get_all(self) -> Tuple[Device]:
        with make_cursor(self.db_path) as cursor:
            cursor.execute(f"SELECT id,name,type FROM {DEVICE_TABLE}")
            result = cursor.fetchall()

        devices = []
        for r in result:
            try:
                device = create_device(r[0], r[1], r[2])
                devices.append(device)
            except DeviceException as e:
                pass
        return tuple(devices)

    def is_exist(self, device_id: DeviceID) -> bool:
        with make_cursor(self.db_path) as cursor:
            # executeはパラメーターにシーケンスを要求するため、引数1つでもこのように指定する
            cursor.execute(
                f"SELECT EXISTS(SELECT 1 FROM {DEVICE_TABLE} WHERE id=?)",
                (device_id.get(),),
            )
            # fetchone() は (0,) または (1,) のタプルを返すので、添字 [0] を取り出して bool にする
            result = bool(cursor.fetchone()[0])
        return result

    def add(
        self,
        id: DeviceID,
        name: str,
        type: str,
        enable_cloud: bool = True,
        hub_device_id: str = "0000",
    ):
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                f"""
                INSERT OR IGNORE INTO {DEVICE_TABLE} (id, name, type, enable_cloud_service, hub_device_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    id.get(),
                    name,
                    type,
                    enable_cloud,
                    hub_device_id,
                ),
            )
