from flask import Flask, render_template
from ApplicationService.device_app_service import DeviceAppService

app = Flask(__name__)

"""ここを移設
def get_devices():
    connection = sqlite3.connect(settings.DEVICES_DB)
    cursor = connection.cursor()

    cursor.execute("SELECT id,type,name FROM devices")
    devices = cursor.fetchall()
    connection.close()

    return ["id", "type", "name"], devices
"""


@app.route("/")
def index():
    # データ要求
    device_app_service = DeviceAppService()
    device_list = device_app_service.get()
    # データ渡し
    return render_template(
        "index.html", columns=device_list.columns, devices=device_list.devices
    )


if __name__ == "__main__":
    app.run(debug=True)
