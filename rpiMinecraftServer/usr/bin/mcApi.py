#!/usr/bin/python3
from flask import Flask, request, jsonify
from mcServer import MinecraftServer

API_PATH = "/api/v1"

app = Flask(__name__)


@app.route(f"{API_PATH}/server/status", methods=["GET"])
def server_status():
    status = "Closed"
    if mcserver.isClossing:
        status = "Clossing"
    elif mcserver.isReady:
        status = "Ready"
    elif mcserver.isRunning:
        status = "Starting"

    return jsonify({"status": status}), 200


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


if __name__ == "__main__":
    confFile = "/etc/productConf/mc.conf"
    mcserver = MinecraftServer(confFile)
    app.run(debug=True, host="0.0.0.0")
