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


@app.route("/light/<device_id>/toggle", methods=["POST"])
def toggle_switch(device_id):
    device_app_service.toggle_switch(str(device_id))
    return redirect(url_for("index"))


@app.route("/light/<device_id>/detail", methods=["GET"])
def detail_setting(device_id):
    return render_template("light.html", device_id=device_id)


@app.route("/light/<device_id>/white", methods=["POST"])
def white_control(device_id):
    brightness = request.form.get("white_brightness")
    color_temp = request.form.get("color_temp")
    device_app_service.white_control(device_id, brightness, color_temp)
    return render_template("light.html", device_id=device_id)


@app.route("/light/<device_id>/color", methods=["POST"])
def color_control(device_id):
    color_hex = request.form.get("color_picker")
    brightness = request.form.get("color_brightness")
    if color_hex and color_hex.startswith("#") and len(color_hex) == 7:
        r = int(color_hex[1:3], 16)
        g = int(color_hex[3:5], 16)
        b = int(color_hex[5:7], 16)
    else:
        r, g, b = 255, 255, 255
    device_app_service.color_control(device_id, Color(r, g, b), brightness)
    return render_template("light.html", device_id=device_id)


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
    group_app_service.toggle_switch(int(group_id))
    return redirect(url_for("index"))


@app.route("/color_adjustment_group", methods=["POST"])
def color_adjustment_group():
    data = request.get_json()
    group_id = int(data.get("group_id"))
    red = data.get("r", 0)
    green = data.get("g", 0)
    blue = data.get("b", 0)
    group_app_service.color_adjustment(group_id, Color(red, green, blue))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
