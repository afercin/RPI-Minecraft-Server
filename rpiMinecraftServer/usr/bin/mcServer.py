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
        self.maxRam = config["SERVER"]["MaxRAM"]
        self.minRam = config["SERVER"]["MinRAM"]

        self.isRunning = False
        self.outputHook = threading.Thread(target=self.getOutput)

    def start(self):
        forgeVersion = "1.12.2-14.23.5.2859"
        forgeFile = "forge-{}.jar".format(forgeVersion)
        if not self.isRunning:
            print("Starting minecraft server...")

            os.chdir(self.minecraftFolder)
            self.minecraftProcess = subprocess.Popen(
                "java -Xmx{} -Xms{} {} -jar '{}' -nogui".format(
                    self.maxRam, self.minRam, self.aditionalArgs, forgeFile),
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                encoding='utf-8',
                errors='replace'
            )
            print("Minecraft server started!")
            self.isRunning = True
            self.outputHook.start()

    def stop(self):
        if self.isRunning:
            print("Stopping server...")
            self.sendCommand("stop")
            self.minecraftProcess.wait()
            print("Server stopped!")
            self.isRunning = False

    def sendCommand(self, command):
        if self.isRunning:
            self.minecraftProcess.communicate(input="{}\n".format(command))

    def getOutput(self):
        print("Hook initialized")
        while self.isRunning:
            realtime_output = self.minecraftProcess.stdout.readline()

            if realtime_output == '' and self.minecraftProcess.poll() is not None:
                break

            if realtime_output:
                self.processOutput(realtime_output.strip())
    
    def processOutput(self, output):
        print(output, flush=True)
        if "[Server thread/INFO] [minecraft/DedicatedServer]: Done" in output:
            print("¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ Mundo listo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


if __name__ == "__main__":
    confFile = "/etc/productConf/mc.conf"

    if "dev" in os.path.abspath(os.getcwd()):
        confFile = "/home/afercin/dev/RPI-Minecraft-Server/rpiMinecraftServer" + confFile

    server = MinecraftServer(confFile)
    server.start()
    input()
    server.stop()
