from utility.exception import GroupException
import sqlite3
from Domain.Group.group_repository import IGroupRepository
from Domain.Group.group import Group, NewGroup, GroupID, GroupName
from Domain.Device.device import DeviceID
from Infra.repository_common import make_cursor


class GroupRepository(IGroupRepository):
    def __init__(self, db_path):
        self.db_path = db_path
        with make_cursor(self.db_path) as cursor:
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

    def add(self, new_group: NewGroup) -> None:
        try:
            with make_cursor(self.db_path) as cursor:
                cursor.execute(
                    """
                    INSERT INTO groups (name)
                    VALUES (?)
                    """,
                    (new_group.name.get(),),
                )

                new_group_id = cursor.lastrowid
                for device_id in new_group.device_ids:
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
        except sqlite3.IntegrityError as e:
            raise GroupException(
                f"DeviceID:{device_id.get()},NewGroupID:{new_group_id},{str(e)}"
            )

    def get_all(self):
        with make_cursor(self.db_path) as cursor:
            cursor.execute("SELECT id,name FROM groups")
            result = cursor.fetchall()

            groups = []
            for r in result:
                group = Group(GroupID(r[0]), GroupName(r[1]))
                groups.append(group)
        return tuple(groups)

    def get_devices(self, group_id: GroupID):
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                """
                SELECT device_id
                FROM group_device
                WHERE group_id = ?
            """,
                (group_id.get(),),
            )

            device_ids = cursor.fetchall()
        return tuple(DeviceID(id[0]) for id in device_ids)

    def is_exist(self, group_id: GroupID) -> bool:
        with make_cursor(self.db_path) as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM groups WHERE id=?)", (group_id.get(),)
            )
            result = bool(cursor.fetchone()[0])
        return result
