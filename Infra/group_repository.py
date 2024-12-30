from Domain.Group.group_repository import IGroupRepository
from Domain.Group.group import Group
from Domain.Device.device import Device
import sqlite3
from typing import List


class InMemoryGroupRepository(IGroupRepository):
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")
        cursor = self.connection.cursor()
        cursor.execute(
            """
                CREATE TABLE groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """
        )
        cursor.execute(
            """
                CREATE TABLE group_device (
                    group_id  INTEGER NOT NULL,
                    device_id TEXT NOT NULL,
                    FOREIGN KEY (group_id)  REFERENCES groups (group_id) ON DELETE CASCADE,
                    FOREIGN KEY (device_id) REFERENCES devices (id) ON DELETE CASCADE,
                    PRIMARY KEY (group_id, device_id)
                )
            """
        )
        self.connection.commit()

    def add(self, devices: List[Device], name: str):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO groups (name)
            VALUES (?)
            """,
            (name,),
        )
        self.connection.commit()

        inserted_group_id = cursor.lastrowid
        for device in devices:
            cursor.execute(
                """
                INSERT INTO group_device (group_id,device_id)
                VALUES (?,?)
                """,
                (
                    inserted_group_id,
                    device,
                ),
            )
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT id,name FROM groups")
        result = cursor.fetchall()

        groups = []
        for r in result:
            group = Group(r[0], r[1])
            groups.append(group)

        return tuple(groups)
