from flask import Flask
from flask_restful import Resource, Api, reqparse
from mcServer import MinecraftServer
import os

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

confFile = "/etc/productConf/mc.conf"

if "dev" in os.path.abspath(os.getcwd()):
    confFile = "/home/afercin/dev/RPI-Minecraft-Server/rpiMinecraftServer" + confFile

mcserver = MinecraftServer(confFile)


class Start(Resource):
    def get(self):
        if mcserver.isRunning:
            return "Minecraft server is already running", 403

        mcserver.start()
        return "Starting minecraft server", 202


class Stop(Resource):
    def get(self):
        if not mcserver.isRunning:
            return "Minecraft server is not running", 403

        if mcserver.isClossing:
            return "Minecraft server is being clossing", 403

        mcserver.stop()
        return "Stopping minecraft server", 202


class GetStatus(Resource):
    def get(self):
        if mcserver.isClossing:
            return "Clossing", 200
        if mcserver.isReady:
            return "Ready", 200
        if mcserver.isRunning:
            return "Starting", 200

        return "Closed", 200

class GetOnlineUsers(Resource):
    def get(self):
        return mcserver.getOnlineUsers()

class GetOutput(Resource):
    def get(self):
        return mcserver.getOutput()

class SendCommand(Resource):
    def post(self, command):
        if not mcserver.isRunning:
            return "Minecraft server is not running", 503
        if not mcserver.isReady:
            return "Minecraft server is not ready", 503

        mcserver.sendCommand(command)
        return "Command send sucessfully", 200


api.add_resource(Start, "/start/")
api.add_resource(Stop, "/stop/")
api.add_resource(GetOnlineUsers, "/online-users/")
api.add_resource(GetStatus, "/status/")
api.add_resource(GetOutput, "/output/")
api.add_resource(SendCommand, "/command/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
