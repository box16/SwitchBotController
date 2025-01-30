import time
import hashlib
import hmac
import base64
import uuid
import os
import json
import requests
from Domain.api_gateway import ISwitchBotGateway
from Domain.Device.device import DeviceID
from Domain.Device.light import Color, Brightness, ColorTemperature


class SwitchBotGateway(ISwitchBotGateway):
    def _create_header(self):
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

    def send_toggle_switch(self, device_id: DeviceID):
        # TODO 結果出した方がいいかも
        header = self._create_header()
        data = json.dumps(
            {
                "commandType": "command",
                "command": "toggle",
                "parameter": "default",
            }
        )

        requests.post(
            f"https://api.switch-bot.com/v1.1/devices/{device_id.get()}/commands",
            headers=header,
            data=data,
        )

    def send_color_control(
        self, device_id: DeviceID, color: Color, brightness: Brightness
    ):
        header = self._create_header()
        data = json.dumps(
            {
                "commandType": "command",
                "command": "setColor",
                "parameter": f"{color.red.get()}:{color.green.get()}:{color.blue.get()}",
            }
        )
        requests.post(
            f"https://api.switch-bot.com/v1.1/devices/{device_id.get()}/commands",
            headers=header,
            data=data,
        )

        data = json.dumps(
            {
                "commandType": "command",
                "command": "setBrightness",
                "parameter": f"{brightness.get()}",
            }
        )
        requests.post(
            f"https://api.switch-bot.com/v1.1/devices/{device_id.get()}/commands",
            headers=header,
            data=data,
        )

    def send_white_control(
        self, device_id: DeviceID, brightness: Brightness, color_temp: ColorTemperature
    ):
        header = self._create_header()
        data = json.dumps(
            {
                "commandType": "command",
                "command": "setBrightness",
                "parameter": f"{brightness.get()}",
            }
        )
        requests.post(
            f"https://api.switch-bot.com/v1.1/devices/{device_id.get()}/commands",
            headers=header,
            data=data,
        )

        data = json.dumps(
            {
                "commandType": "command",
                "command": "setColorTemperature",
                "parameter": f"{color_temp.get()}",
            }
        )
        requests.post(
            f"https://api.switch-bot.com/v1.1/devices/{device_id.get()}/commands",
            headers=header,
            data=data,
        )


class FakeSwitchBotGateway(ISwitchBotGateway):
    def send_toggle_switch(self, device_id: DeviceID):
        pass

    def send_color_control(self, device_id: DeviceID, color: Color):
        pass
