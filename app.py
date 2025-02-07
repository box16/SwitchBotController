from flask import Flask, render_template, redirect, url_for, request
from ApplicationService.Device.device_app_service import DeviceAppService, DtODevice
from ApplicationService.Group.group_app_service import (
    LightGroupAppService,
    CreateGroupCommand,
    DtOGroup,
    UpdateGroupCommand,
)
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
light_group_app_service = LightGroupAppService(
    group_repository, device_repository, SwitchBotGateway()
)


@app.route("/", methods=["GET"])
def index():
    devices: Tuple[DtODevice] = device_app_service.get_all()
    light_groups: Tuple[DtOGroup] = light_group_app_service.get_all()
    return render_template(
        "index.html",
        devices=devices,
        light_groups=light_groups,
    )


@app.route("/light/<device_id>/toggle", methods=["POST"])
def toggle_switch(device_id):
    device_app_service.toggle_switch(str(device_id))
    return redirect(url_for("index"))


@app.route("/light_group/<group_id>/on", methods=["POST"])
def switch_on(group_id):
    light_group_app_service.switch_on(group_id)
    return redirect(url_for("index"))


@app.route("/light_group/<group_id>/off", methods=["POST"])
def switch_off(group_id):
    light_group_app_service.switch_off(group_id)
    return redirect(url_for("index"))


@app.route("/light/<device_id>/detail", methods=["GET"])
def detail_setting(device_id):
    return render_template("light.html", device_id=device_id)


@app.route("/light_group/<group_id>/detail", methods=["GET"])
def detail_setting_group(group_id):
    return render_template("light_group.html", group_id=group_id)


@app.route("/light/<device_id>/white", methods=["POST"])
def white_control(device_id):
    brightness = request.form.get("white_brightness")
    color_temp = request.form.get("color_temp")
    device_app_service.white_control(device_id, brightness, color_temp)
    return render_template("light.html", device_id=device_id)


@app.route("/light_group/<group_id>/white", methods=["POST"])
def white_control_group(group_id):
    brightness = request.form.get("white_brightness")
    color_temp = request.form.get("color_temp")
    light_group_app_service.white_control(group_id, brightness, color_temp)
    return render_template("light_group.html", group_id=group_id)


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
    device_app_service.color_control(device_id, Color(r, g, b), brightness)
    return render_template("light.html", device_id=device_id)


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
    light_group_app_service.color_control(group_id, Color(r, g, b), brightness)
    return render_template("light_group.html", group_id=group_id)


@app.route("/device/<device_id>/change_name", methods=["POST"])
def change_name(device_id):
    new_name = request.form.get("device_name")
    device_app_service.change_name(device_id, new_name)
    return redirect(url_for("index"))


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
    group = light_group_app_service.get_by_id(group_id)

    if request.method == "GET":
        current_devices = light_group_app_service.get_member_by_id(group_id)
        return render_template(
            "edit_light_group.html",
            group=group,
            current_device=current_devices,
        )

    if request.method == "POST":
        new_name = request.form.get("group_name")
        selected_devices = request.form.getlist(
            "selected_devices"
        )  # 選択されたデバイスIDのリスト

        # 現在のグループメンバーを文字列の集合として取得
        from Domain.Group.group import GroupID

        current_devices = group_repository.get_device_ids(GroupID(group_id))
        current_device_ids = {d.get() for d in current_devices}
        new_device_ids = set(selected_devices)

        # 追加すべきデバイスと削除すべきデバイスを算出
        add_devices = tuple(new_device_ids - current_device_ids)
        remove_devices = tuple(current_device_ids - new_device_ids)

        # グループ名が変更されていれば更新
        if new_name and new_name != group.name:
            light_group_app_service.change_name(group_id, new_name)

        # グループメンバーの追加／削除を実行
        update_command = UpdateGroupCommand(add_devices, remove_devices)
        light_group_app_service.update_group(group_id, update_command)

        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
