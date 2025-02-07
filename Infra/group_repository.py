from utility.exception import GroupException
import sqlite3
from Domain.Group.group_repository import IGroupRepository
from Domain.Group.group import Group, NewGroup, GroupID, GroupName, GroupType
from Domain.Group.group_factory import create_group
from Domain.Device.device import DeviceID
from Infra.repository_common import (
    make_cursor,
    GROUP_TABLE,
    DEVICE_TABLE,
    GROUP_DEVICE_TABLE,
)
from typing import Tuple


class GroupRepository(IGroupRepository):
    def __init__(self, db_path):
        self.db_path = db_path
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS {GROUP_TABLE} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        type TEXT NOT NULL
                    )
                """
            )
            cursor.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS {GROUP_DEVICE_TABLE} (
                        group_id  INTEGER NOT NULL,
                        device_id TEXT NOT NULL,
                        FOREIGN KEY (group_id)  REFERENCES {GROUP_TABLE} (id) ON DELETE CASCADE,
                        FOREIGN KEY (device_id) REFERENCES {DEVICE_TABLE} (id) ON DELETE CASCADE,
                        PRIMARY KEY (group_id, device_id)
                    )
                """
            )

    def add(self, new_group: NewGroup) -> None:
        try:
            with make_cursor(self.db_path) as cursor:
                cursor.execute(
                    f"""
                    INSERT INTO {GROUP_TABLE} (name,type)
                    VALUES (?, ?)
                    """,
                    (new_group.name.get(), new_group.type.name),
                )

                new_group_id = cursor.lastrowid
                for device_id in new_group.device_ids:
                    cursor.execute(
                        f"""
                        INSERT INTO {GROUP_DEVICE_TABLE} (group_id,device_id)
                        VALUES (?,?)
                        """,
                        (
                            new_group_id,
                            device_id.get(),
                        ),
                    )
        except sqlite3.IntegrityError as e:
            raise GroupException(
                f"DeviceID:{device_id.get()},NewGroupID:{new_group_id},{str(e)}"
            )

    def get_all(self):
        with make_cursor(self.db_path) as cursor:
            cursor.execute(f"SELECT id,name,type FROM {GROUP_TABLE}")
            result = cursor.fetchall()

            groups = tuple(create_group(r[0], r[1], r[2]) for r in result)
        return groups

    def get_device_ids(self, group_id: GroupID):
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                f"""
                SELECT device_id
                FROM {GROUP_DEVICE_TABLE}
                WHERE group_id = ?
            """,
                (group_id.get(),),
            )

            device_ids = cursor.fetchall()
        return tuple(DeviceID(id[0]) for id in device_ids)

    def is_exist(self, group_id: GroupID) -> bool:
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                f"SELECT EXISTS(SELECT 1 FROM {GROUP_TABLE} WHERE id=?)",
                (group_id.get(),),
            )
            result = bool(cursor.fetchone()[0])
        return result

    def get_by_type(self, type: GroupType) -> Tuple[Group]:
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                f"SELECT id,name,type FROM {GROUP_TABLE} WHERE type=?",
                (type.name,),
            )
            result = cursor.fetchall()
        groups = [create_group(r[0], r[1], r[2]) for r in result]
        return groups

    def change_name(self, id: GroupID, new_name: GroupName):
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                f"UPDATE {GROUP_TABLE} SET name = ? WHERE id=?",
                (
                    new_name.get(),
                    id.get(),
                ),
            )

    def add_device(self, id: GroupID, new_devices: tuple[DeviceID]):
        try:
            with make_cursor(self.db_path) as cursor:
                for device in new_devices:
                    cursor.execute(
                        f"""
                        INSERT INTO {GROUP_DEVICE_TABLE} (group_id,device_id)
                        VALUES (?,?)
                        """,
                        (
                            id.get(),
                            device.get(),
                        ),
                    )
        except sqlite3.IntegrityError as e:
            raise GroupException(f"GroupID:{id.get()},DeviceID:{device.id()},{str(e)}")

    def remove_device(self, id: GroupID, remove_devices: tuple[DeviceID]):
        try:
            with make_cursor(self.db_path) as cursor:
                for device in remove_devices:
                    cursor.execute(
                        f"""
                            DELETE FROM {GROUP_DEVICE_TABLE} WHERE group_id = ? AND device_id = ?
                            """,
                        (
                            id.get(),
                            device.get(),
                        ),
                    )
        except sqlite3.IntegrityError as e:
            raise GroupException(f"GroupID:{id.get()},DeviceID:{device.id()},{str(e)}")

    def get_by_id(self, id: GroupID) -> Group:
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                f"SELECT id,name,type FROM {GROUP_TABLE} WHERE id=?",
                (id.get(),),
            )
            result = cursor.fetchone()
        group = create_group(result[0], result[1], result[2])
        return group
