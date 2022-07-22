import subprocess
import threading
import os
import configparser


class MinecraftServer:

    def __init__(self, confFile):
        config = configparser.ConfigParser()
        config.read(confFile)

        self.minecraftFolder = config["SERVER"]["MinecraftFolder"]
        self.aditionalArgs = config["SERVER"]["AditionalArgs"]
        self.forgeVersion = config["SERVER"]["ForgeVersion"]
        self.onlineUsers = []

        self.reset()

    def reset(self):
        self.isRunning = False
        self.isClossing = False
        self.isReady = False
        self.output = ""

    def start(self):
        if not self.isRunning:
            self.reset()
            print("Starting minecraft server...")

            os.chdir(self.minecraftFolder)
            self.minecraftProcess = subprocess.Popen(
                f"{self.minecraftFolder}/run.sh {self.aditionalArgs}",
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                encoding='utf-8',
                errors='replace'
            )
            print("Minecraft server started!")
            self.isRunning = True
            self.outputHook = threading.Thread(target=self.captureOutput)
            self.outputHook.start()

    def stop(self):
        def stopping():
            self.sendCommand("stop")
            self.minecraftProcess.wait()
            print("Server stopped!")
            self.reset()

        if self.isRunning:
            print("Stopping server...")
            self.isClossing = True
            time = 5
            threading.Thread(target=stopping).start()

    def sendCommand(self, command):
        if self.isRunning:
            self.minecraftProcess.communicate(input="{}\n".format(command))

    def captureOutput(self):
        def getUserName(output, type):
            return output.split(": ")[1].split(type)[0]

        def processOutput(output):
            self.output += "{}\n".format(output)
            print(output, flush=True)
            if "[Server thread/INFO] [minecraft/DedicatedServer]: Done" in output:
                self.isReady = True

            if "joined" in output:
                self.onlineUsers.append(getUserName(output, " joined"))
            
            if "left" in output:
                self.onlineUsers.remove(getUserName(output, " left"))
        
        print("Hook initialized")
        while self.isRunning:
            realtime_output = self.minecraftProcess.stdout.readline()

            if realtime_output == '' and self.minecraftProcess.poll() is not None:
                break

            if realtime_output:
                processOutput(realtime_output.strip())

    def getOutput(self):
        return self.output
    
    def getOnlineUsers(self):
        return self.onlineUsers


if __name__ == "__main__":
    confFile = "/etc/productConf/mc.conf"

    if "dev" in os.path.abspath(os.getcwd()):
        confFile = "/home/afercin/dev/RPI-Minecraft-Server/rpiMinecraftServer" + confFile

    server = MinecraftServer(confFile)
    server.start()
    input()
    server.stop()
