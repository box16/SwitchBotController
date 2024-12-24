import json
import requests


from header_creator import create_header

api_header = create_header()
response = requests.get("https://api.switch-bot.com/v1.1/devices", headers=api_header)
response_data = response.json()

if not response_data.get("statusCode") == 100:
    print(f"デバイスリストの取得に失敗 statusCode:{response_data.get("statusCode")}")
    exit()

device_list = response_data.get("body", {}).get("deviceList", [])
output_file = "devices.json"
with open(output_file, "w") as f:
    json.dump(device_list, f, indent=4)
