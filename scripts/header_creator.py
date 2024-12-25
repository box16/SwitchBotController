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
