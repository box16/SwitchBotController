from flask import Flask, render_template, redirect, url_for, request
from ApplicationService.Device.device_app_service import (
    DeviceAppService,
    DtODevice,
)
from ApplicationService.Group.group_app_service import (
    LightGroupAppService,
    CreateGroupCommand,
    DtOGroup,
    UpdateGroupCommand,
)
from ApplicationService.Device.light_app_service import DtOColor, LightAppService
from Infra.device_repository import DeviceRepository
from Infra.api_gateway import SwitchBotGateway
from Infra.group_repository import GroupRepository
from typing import Tuple
from utility.exception import GroupException
import os

app = Flask(__name__)
group_repository = GroupRepository(os.getenv("SWITCHBOT_DB_PATH"))
device_repository = DeviceRepository(os.getenv("SWITCHBOT_DB_PATH"))
device_app_service = DeviceAppService(device_repository)
light_app_service = LightAppService(device_repository, SwitchBotGateway())
light_group_app_service = LightGroupAppService(
    group_repository, device_repository, SwitchBotGateway()
)


# 管理システム
@app.route("/", methods=["GET"])
def index():
    devices: Tuple[DtODevice] = device_app_service.get_all()
    light_groups: Tuple[DtOGroup] = light_group_app_service.get_all()
    return render_template(
        "index.html",
        devices=devices,
        light_groups=light_groups,
    )


# デバイス
@app.route("/device/<device_id>/change_name", methods=["POST"])
def change_name(device_id):
    new_name = request.form.get("device_name")
    device_app_service.change_name(device_id, new_name)
    return redirect(url_for("index"))


# ライト
@app.route("/light/<device_id>/toggle", methods=["POST"])
def toggle_switch(device_id):
    light_app_service.toggle_switch(str(device_id))
    return redirect(url_for("index"))


@app.route("/light/<device_id>/detail", methods=["GET"])
def detail_setting(device_id):
    return render_template("light.html", device_id=device_id)


@app.route("/light/<device_id>/white", methods=["POST"])
def white_control(device_id):
    brightness = request.form.get("white_brightness")
    color_temp = request.form.get("color_temp")
    light_app_service.white_control(device_id, brightness, color_temp)
    return render_template("light.html", device_id=device_id)


@app.route("/light/<device_id>/color", methods=["POST"])
def color_control(device_id):
    color_hex = request.form.get("color_picker")
    brightness = request.form.get("color_brightness")
    # TODO : これ何とかしたい
    if color_hex and color_hex.startswith("#") and len(color_hex) == 7:
        r = int(color_hex[1:3], 16)
        g = int(color_hex[3:5], 16)
        b = int(color_hex[5:7], 16)
    else:
        r, g, b = 255, 255, 255
    light_app_service.color_control(device_id, DtOColor(r, g, b), brightness)
    return render_template("light.html", device_id=device_id)


# グループ
@app.route("/group/<group_id>/delete", methods=["POST"])
def delete_group(group_id):
    light_group_app_service.delete_group(group_id)
    return redirect(url_for("index"))


# ライトグループ
@app.route("/light_group/<group_id>/on", methods=["POST"])
def switch_on(group_id):
    light_group_app_service.switch_on(group_id)
    return redirect(url_for("index"))


@app.route("/light_group/<group_id>/off", methods=["POST"])
def switch_off(group_id):
    light_group_app_service.switch_off(group_id)
    return redirect(url_for("index"))


@app.route("/light_group/<group_id>/detail", methods=["GET"])
def detail_setting_group(group_id):
    return render_template("light_group.html", group_id=group_id)


@app.route("/light_group/<group_id>/white", methods=["POST"])
def white_control_group(group_id):
    brightness = request.form.get("white_brightness")
    color_temp = request.form.get("color_temp")
    light_group_app_service.white_control(group_id, brightness, color_temp)
    return render_template("light_group.html", group_id=group_id)


@app.route("/light_group/<group_id>/color", methods=["POST"])
def color_control_group(group_id):
    color_hex = request.form.get("color_picker")
    brightness = request.form.get("color_brightness")
    # TODO : これ何とかしたい
    if color_hex and color_hex.startswith("#") and len(color_hex) == 7:
        r = int(color_hex[1:3], 16)
        g = int(color_hex[3:5], 16)
        b = int(color_hex[5:7], 16)
    else:
        r, g, b = 255, 255, 255
    light_group_app_service.color_control(group_id, DtOColor(r, g, b), brightness)
    return render_template("light_group.html", group_id=group_id)


@app.route("/create_light_group", methods=["GET", "POST"])
def create_light_group():
    if request.method == "GET":
        # TODO : Lightのみ出力
        devices: Tuple[DtODevice] = device_app_service.get_all()
        return render_template("create_group.html", devices=devices)

    if request.method == "POST":
        try:
            selected_device = request.form.getlist("selected")
            group_name = request.form.get("name")
            command = CreateGroupCommand(group_name, selected_device)
            light_group_app_service.create_group(command)
        except GroupException as e:
            print(f"グループ作成に失敗しました : {str(e)}")
        return redirect(url_for("index"))


@app.route("/light_group/<group_id>/edit", methods=["GET", "POST"])
def edit_group(group_id):
    if request.method == "GET":
        group = light_group_app_service.get_by_id(group_id)
        current_devices = light_group_app_service.get_member_by_id(group_id)
        light_devices = device_app_service.get_by_type("LIGHT")

        not_group_member = set(light_devices) - set(current_devices)
        return render_template(
            "edit_light_group.html",
            group=group,
            current_device=current_devices,
            not_group_member=not_group_member,
        )

    if request.method == "POST":
        group = light_group_app_service.get_by_id(group_id)

        new_name = request.form.get("group_name")
        if group.name != new_name:
            light_group_app_service.change_name(group_id, new_name)

        selected_ids = set(request.form.getlist("selected_devices"))
        current_devices = light_group_app_service.get_member_by_id(group_id)
        current_ids = set([d.id for d in current_devices])

        add_devices = selected_ids - current_ids
        remove_devices = current_ids - selected_ids
        command = UpdateGroupCommand(tuple(add_devices), tuple(remove_devices))
        light_group_app_service.update_group(group_id, command)

        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
