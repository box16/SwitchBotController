from flask import Flask, render_template, redirect, url_for
from ApplicationService.Device.device_app_service import DeviceAppService
from ApplicationService.Device.dto_device import DeviceList
from Infra.device_repository import DeviceRepository
from Infra.api_gateway import SwitchBotGateway

app = Flask(__name__)
device_app_service = DeviceAppService(DeviceRepository(), SwitchBotGateway())


@app.route("/")
def index():
    device_list: DeviceList = device_app_service.get_all()
    return render_template(
        "index.html", columns=device_list.columns, devices=device_list.devices
    )


@app.route("/toggle/<device_id>", methods=["POST"])
def toggle_switch(device_id):
    device_app_service.toggle_switch(device_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
