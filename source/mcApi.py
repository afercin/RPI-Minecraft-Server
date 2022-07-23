#!/usr/bin/python3
from flask import Flask, request, jsonify, send_file
from mcServer import MinecraftServer
from werkzeug import secure_filename
import configparser
import psutil
import os

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("/etc/productConf/mc.conf")

MOD_FOLDER = f"{config['SERVER']['MinecraftFolder']}/mods"
API_PATH = config['API']['Path']
API_PORT = config['API']['Port']


@app.route(f"{API_PATH}/server/status", methods=["GET"])
def server_status():
    status = "Closed"
    if mcserver.isClossing:
        status = "Clossing"
    elif mcserver.isReady:
        status = "Ready"
    elif mcserver.isRunning:
        status = "Starting"

    return jsonify({
        "status": status,
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent
    }), 200


@app.route(f"{API_PATH}/server/start", methods=["GET"])
def server_start():
    if mcserver.isRunning:
        return jsonify({"msg": "Minecraft server is already running"}), 403

    mcserver.start()
    return jsonify({"msg": "Starting minecraft server"}), 202


@app.route(f"{API_PATH}/server/stop", methods=["GET"])
def server_stop():
    if not mcserver.isRunning:
        return jsonify({"msg": "Minecraft server is not running"}), 403

    if not mcserver.isRunning:
        return jsonify({"msg": "Minecraft server is being clossing"}), 403

    mcserver.stop()
    return jsonify({"msg": "Stopping minecraft server"}), 202


@app.route(f"{API_PATH}/server/players", methods=["GET"])
def get_server_players():
    return jsonify(mcserver.getOnlineUsers()), 200


@app.route(f"{API_PATH}/server/output", methods=["GET"])
def get_server_output():
    return jsonify({"output": mcserver.getOutput()}), 200


@app.route(f"{API_PATH}/server/command", methods=["POST"])
def send_server_command():
    try:
        command = request.args["command"]

        if not mcserver.isRunning:
            return jsonify({"msg": "Minecraft server is not running"}), 403
        if not mcserver.isReady:
            return jsonify({"msg": "Minecraft server is not ready"}), 403

        mcserver.sendCommand(command)
        return jsonify({"msg": "Command send sucessfully"}), 200

    except:
        return jsonify({"msg": "Missing param 'command'"}), 403


@app.route(f"{API_PATH}/server/mods/list", methods=["GET"])
def mod_list():
    return jsonify([f for f in os.listdir(MOD_FOLDER) if os.path.isfile(os.path.join(MOD_FOLDER, f))]), 200


@app.route(f"{API_PATH}/server/mods/download/<path:mod>", methods=["GET"])
def download(mod):
    if os.path.isfile(f"{MOD_FOLDER}/{mod}"):
        return send_file(f"{MOD_FOLDER}/{mod}", as_attachment=True)
    else:
        return jsonify({"msg": f"Invalid mod name '{mod}'"}), 403


@app.route(f"{API_PATH}/server/mods/upload", methods=["POST"])
def upload():
    mod = request.files['mod']
    mod.save(secure_filename(mod.filename))
    return jsonify({"msg": "Mod uploaded successfully"}), 200


if __name__ == "__main__":
    mcserver = MinecraftServer(config)
    app.run(debug=True, host="0.0.0.0", port=API_PORT)
