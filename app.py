from flask import Flask, render_template
import sqlite3
import settings

app = Flask(__name__)


def get_devices():
    connection = sqlite3.connect(settings.DEVICES_DB)
    cursor = connection.cursor()

    cursor.execute("SELECT id,type,name FROM devices")
    devices = cursor.fetchall()
    connection.close()

    return ["id", "type", "name"], devices


@app.route("/")
def index():
    columns, devices = get_devices()
    return render_template("index.html", columns=columns, devices=devices)


if __name__ == "__main__":
    app.run(debug=True)
