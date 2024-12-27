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
