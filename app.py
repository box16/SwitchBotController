from flask import Flask, render_template, redirect, url_for
from ApplicationService.Device.device_app_service import DeviceAppService
from ApplicationService.Device.dto_device import DeviceList
from ApplicationService.Group.group_app_service import GroupAppService
from ApplicationService.Group.dto_group import Group
from Infra.device_repository import DeviceRepository
from Infra.api_gateway import SwitchBotGateway
from Infra.group_repository import GroupRepository
from typing import Tuple

app = Flask(__name__)
device_app_service = DeviceAppService(DeviceRepository(), SwitchBotGateway())
group_app_service = GroupAppService(GroupRepository(), SwitchBotGateway())


@app.route("/")
def index():
    device_list: DeviceList = device_app_service.get_all()
    group_list: Tuple[Group] = group_app_service.get_all()
    return render_template(
        "index.html",
        columns=device_list.columns,
        devices=device_list.devices,  # ここ修正
        groups=group_list,
    )


@app.route("/toggle/<device_id>", methods=["POST"])
def toggle_switch(device_id):
    device_app_service.toggle_switch(device_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
