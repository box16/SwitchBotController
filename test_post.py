import requests
import pprint
import json
from header_creator import create_header

device_file = "devices.json"
with open(device_file, "r", encoding="utf-8") as f:
    devices = json.load(f)

color_bulb = None
for device in devices:
    if device.get("deviceType") == "Color Bulb":
        color_bulb = device.get("deviceId")
        break

api_header = create_header()
params = {
    "commandType": "command",
    "command": "setColor",
    "parameter": "64:00:00",
}
json_params = json.dumps(params)
response = requests.post(
    f"https://api.switch-bot.com/v1.1/devices/{color_bulb}/commands",
    headers=api_header,
    data=json_params,
)
