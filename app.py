from flask import Flask, render_template, redirect, url_for, request
from ApplicationService.Device.device_app_service import DeviceAppService
from ApplicationService.Device.device_dto import Device
from ApplicationService.Group.group_app_service import GroupAppService
from ApplicationService.Group.group_dto import Group
from ApplicationService.Group.group_command import CreateGroupCommand
from ApplicationService.color_dto import Color
from Infra.device_repository import DeviceRepository
from Infra.api_gateway import SwitchBotGateway
from Infra.group_repository import GroupRepository
from typing import Tuple
from utility.exception import GroupException
import os

app = Flask(__name__)
group_repository = GroupRepository(os.getenv("SWITCHBOT_DB_PATH"))
device_repository = DeviceRepository(os.getenv("SWITCHBOT_DB_PATH"))
device_app_service = DeviceAppService(device_repository, SwitchBotGateway())
group_app_service = GroupAppService(
    group_repository, device_repository, SwitchBotGateway()
)


@app.route("/", methods=["GET"])
def index():
    devices: Tuple[Device] = device_app_service.get_all()
    groups: Tuple[Group] = group_app_service.get_all()
    return render_template(
        "index.html",
        devices=devices,
        groups=groups,
    )


@app.route("/device/<device_id>/toggle", methods=["POST"])
def toggle_switch(device_id):
    device_app_service.toggle_switch(device_id)
    return redirect(url_for("index"))


@app.route("/create_group", methods=["GET", "POST"])
def create_group():
    if request.method == "GET":
        devices: Tuple[Device] = device_app_service.get_all()
        return render_template("create_group.html", devices=devices)

    if request.method == "POST":
        try:
            selected_device = request.form.getlist("selected")
            group_name = request.form.get("name")
            command = CreateGroupCommand(group_name, selected_device)
            group_app_service.create_group(command)
        except GroupException as e:
            print(f"グループ作成に失敗しました : {str(e)}")
        return redirect(url_for("index"))


@app.route("/group/<group_id>/toggle", methods=["POST"])
def toggle_switch_group(group_id):
    group_app_service.toggle_switch(group_id)
    return redirect(url_for("index"))


@app.route("/device/<device_id>/color", methods=["POST"])
def color_adjustment(device_id):
    red = request.form.get("red", type=int)
    green = request.form.get("green", type=int)
    blue = request.form.get("blue", type=int)
    device_app_service.color_adjstment(device_id, Color(red, green, blue))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
