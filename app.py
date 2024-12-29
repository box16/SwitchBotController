from flask import Flask, render_template
from ApplicationService.device_app_service import DeviceAppService
from ApplicationService.dto_device import DeviceList
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


if __name__ == "__main__":
    app.run(debug=True)
