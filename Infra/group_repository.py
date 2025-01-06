from utility.exception import GroupException
import sqlite3
import os
from Domain.Group.group_repository import IGroupRepository
from Domain.Group.group import Group, NewGroup, GroupID, GroupName
from Domain.Device.device import DeviceID


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

    def add(self, new_group: NewGroup) -> None:
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            connection.execute("BEGIN TRANSACTION")
            cursor.execute(
                """
                INSERT INTO groups (name)
                VALUES (?)
                """,
                (new_group.name.get(),),
            )

            new_group_id = cursor.lastrowid
            for device_id in new_group.device_list:
                cursor.execute(
                    """
                    INSERT INTO group_device (group_id,device_id)
                    VALUES (?,?)
                    """,
                    (
                        new_group_id,
                        device_id.get(),
                    ),
                )
            connection.commit()
        except sqlite3.IntegrityError as e:
            connection.rollback()
            raise GroupException(
                f"DeviceID:{device_id.get()},NewGroupID:{new_group_id},{str(e)}"
            )

    def get_all(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT id,name FROM groups")
        result = cursor.fetchall()

        groups = []
        for r in result:
            group = Group(GroupID(r[0]), GroupName(r[1]))
            groups.append(group)

        return tuple(groups)

    def get_devices(self, group_id: GroupID):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT device_id
            FROM group_device
            WHERE group_id = ?
        """,
            (group_id.get(),),
        )

        device_ids = cursor.fetchall()
        if not device_ids:
            raise GroupException(f"グループIDが存在しません")

        return tuple(DeviceID(id[0]) for id in device_ids)


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

    def add(self, new_group: NewGroup):
        try:
            self.connection.execute("BEGIN TRANSACTION")
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT INTO groups (name)
                VALUES (?)
                """,
                (new_group.name.get(),),
            )

            new_group_id = cursor.lastrowid
            for device_id in new_group.device_list:
                cursor.execute(
                    """
                    INSERT INTO group_device (group_id,device_id)
                    VALUES (?,?)
                    """,
                    (
                        new_group_id,
                        device_id.get(),
                    ),
                )
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            self.connection.rollback()
            raise GroupException(
                f"DeviceID:{device_id.get()},NewGroupID:{new_group_id},{str(e)}"
            )

    def get_all(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT id,name FROM groups")
        result = cursor.fetchall()

        groups = []
        for r in result:
            group = Group(GroupID(r[0]), GroupName(r[1]))
            groups.append(group)

        return tuple(groups)

    def get_devices(self, group_id: GroupID):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT device_id
            FROM group_device
            WHERE group_id = ?
        """,
            (group_id.get(),),
        )

        device_ids = cursor.fetchall()
        if not device_ids:
            raise GroupException(f"グループIDが存在しません")

        return tuple(DeviceID(id[0]) for id in device_ids)
