from logUtils import logUtils
import subprocess
import threading
import os
import configparser


class MinecraftServer:

    def __init__(self, confFile):
        config = configparser.ConfigParser()
        config.read(confFile)
        self.log = logUtils(verbose=True)

        self.minecraftFolder = config["SERVER"]["MinecraftFolder"]
        self.forgeVersion = config["SERVER"]["ForgeVersion"]
        self.aditionalArgs = config["SERVER"]["AditionalArgs"]
        self.maxRam = config["SERVER"]["MaxRAM"]
        self.minRam = config["SERVER"]["MinRAM"]

        self.isRunning = False
        self.outputHook = threading.Thread(target=self.getOutput)

    def start(self):
        if not self.isRunning:
            forgeFile = "forge-{}.jar".format(self.forgeVersion)
            self.log.info("Starting minecraft server...")

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
            self.log.ok("Minecraft server started!")
            self.isRunning = True
            self.outputHook.start()

    def stop(self):
        if self.isRunning:
            self.log.info("Stopping server...")
            self.sendCommand("stop")
            self.minecraftProcess.wait()
            self.log.ok("Server stopped!")
            self.isRunning = False

    def sendCommand(self, command):
        if self.isRunning:
            self.minecraftProcess.communicate(input="{}\n".format(command))

    def getOutput(self):
        self.log.info("Hook initialized")
        while self.isRunning:
            realtime_output = self.minecraftProcess.stdout.readline()

            if realtime_output == '' and self.minecraftProcess.poll() is not None:
                break

            if realtime_output:
                self.processOutput(realtime_output.strip())
    
    def processOutput(self, output):
        print(output, flush=True)
        if "[Server thread/INFO] [minecraft/DedicatedServer]: Done" in output:            
            self.log.ok("¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ Mundo listo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


if __name__ == "__main__":
    confFile = "/etc/productConf/mc.conf"

    if "dev" in os.path.abspath(os.getcwd()):
        confFile = "/home/afercin/dev/RPI-Minecraft-Server/rpiMinecraftServer" + confFile

    server = MinecraftServer(confFile)
    server.start()
    input()
    server.stop()
