import requests
import sqlite3
import time
import hashlib
import hmac
import base64
import uuid
import os

def create_header():
    token = os.getenv("SWITCHBOT_TOKEN")
    time_stamp = int(round(time.time() * 1000))
    nonce = uuid.uuid4()
    message = bytes(f"{token}{time_stamp}{nonce}", "utf-8")

    secret_key = os.getenv("SWITCHBOT_SECRET_KEY")
    secret_key = bytes(secret_key, "utf-8")
    sign = base64.b64encode(
        hmac.new(secret_key, msg=message, digestmod=hashlib.sha256).digest()
    )

    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "charset": "utf8",
        "t": str(time_stamp),
        "sign": str(sign, "utf-8"),
        "nonce": str(nonce),
    }

# APIよりデバイス一覧の取得
api_header = create_header()
response = requests.get("https://api.switch-bot.com/v1.1/devices", headers=api_header)
response_data = response.json()

if not response_data.get("statusCode") == 100:
    print(f"デバイスリストの取得に失敗 statusCode:{response_data.get('statusCode')}")
    exit()

device_ids = response_data.get("body", {}).get("deviceList", [])

# 取得したデバイス一覧をDBに記録
connection = sqlite3.connect(os.getenv("SWITCHBOT_DB_PATH"))
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

for device in device_ids:
    try:
        # ?を使ったデータ挿入であればSQLインジェクション対策や特殊文字のエスケープもできる
        cursor.execute(
            """
            INSERT OR IGNORE INTO devices (id, name, type, enable_cloud_service, hub_device_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                device["deviceId"],
                device["deviceName"],
                device["deviceType"],
                device["enableCloudService"],
                device["hubDeviceId"],
            ),
        )
    except sqlite3.IntegrityError as e:
        print(f"Insertエラー {device['deviceId']}: {e}")

connection.commit()
connection.close()
