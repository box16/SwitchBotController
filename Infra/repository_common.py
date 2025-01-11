import sqlite3
from contextlib import contextmanager

DEVICE_TABLE = "devices"
GROUP_TABLE = "groups"
GROUP_DEVICE_TABLE = "group_device"


@contextmanager
def make_cursor(db_path: str):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    try:
        connection.execute("BEGIN TRANSACTION")
        yield cursor
    except sqlite3.IntegrityError as e:
        connection.rollback()
        connection.close()
        raise e
    finally:
        connection.commit()
        connection.close()
