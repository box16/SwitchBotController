from Domain.Group.group_repository import IGroupRepository
from Domain.Group.group import Group
from Domain.Device.device import Device
from utility.exception import DeviceNotFound
import sqlite3
from typing import List
import os


class GroupRepository(IGroupRepository):
    def __init__(self):
        self_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self_dir, "devices.db")

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """
        )
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS group_device (
                    group_id  INTEGER NOT NULL,
                    device_id TEXT NOT NULL,
                    FOREIGN KEY (group_id)  REFERENCES groups (id) ON DELETE CASCADE,
                    FOREIGN KEY (device_id) REFERENCES devices (id) ON DELETE CASCADE,
                    PRIMARY KEY (group_id, device_id)
                )
            """
        )
        connection.commit()
        connection.close()

    def add(self, device_id_list: List[Device], name: str) -> None:
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            connection.execute("BEGIN TRANSACTION")
            cursor.execute(
                """
                INSERT INTO groups (name)
                VALUES (?)
                """,
                (name,),
            )

            new_group_id = cursor.lastrowid
            for device_id in device_id_list:
                cursor.execute(
                    """
                    INSERT INTO group_device (group_id,device_id)
                    VALUES (?,?)
                    """,
                    (
                        new_group_id,
                        device_id,
                    ),
                )
            connection.commit()
        except sqlite3.IntegrityError as e:
            connection.rollback()
            print(f"存在しないデバイスIDが指定されました: {e}")
            raise DeviceNotFound

    def get_all(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT id,name FROM groups")
        result = cursor.fetchall()

        groups = []
        for r in result:
            group = Group(r[0], r[1])
            groups.append(group)

        return tuple(groups)


class InMemoryGroupRepository(IGroupRepository):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
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
                    FOREIGN KEY (group_id)  REFERENCES groups (id) ON DELETE CASCADE,
                    FOREIGN KEY (device_id) REFERENCES devices (id) ON DELETE CASCADE,
                    PRIMARY KEY (group_id, device_id)
                )
            """
        )
        self.connection.commit()

    def add(self, device_id_list: List[Device], name: str):
        try:
            self.connection.execute("BEGIN TRANSACTION")
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT INTO groups (name)
                VALUES (?)
                """,
                (name,),
            )

            new_group_id = cursor.lastrowid
            for device_id in device_id_list:
                cursor.execute(
                    """
                    INSERT INTO group_device (group_id,device_id)
                    VALUES (?,?)
                    """,
                    (
                        new_group_id,
                        device_id,
                    ),
                )
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            self.connection.rollback()
            print(f"存在しないデバイスIDが指定されました: {e}")
            raise DeviceNotFound

    def get_all(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT id,name FROM groups")
        result = cursor.fetchall()

        groups = []
        for r in result:
            group = Group(r[0], r[1])
            groups.append(group)

        return tuple(groups)
