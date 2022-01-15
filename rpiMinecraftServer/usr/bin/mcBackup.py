from logUtils import logUtils
from datetime import datetime
import os
import tarfile
import threading


class mcBackup:
    def __init__(self, mcFolder, backupFolder, maxBackups, delay, backupOnExit, verbose=False):
        self.log = logUtils(verbose=verbose)

        self.mcFolder = mcFolder
        self.backupFolder = backupFolder
        self.maxBackups = maxBackups
        self.delay = delay
        self.backupOkExit = backupOnExit

        self.end = True
        self.creatingBackup = False
        self.process = threading.Thread(target=self.backupProcess)
        self.cond = threading.Condition()

    def start(self):
        if self.end:
            self.end = False
            self.process.start()

    def stop(self):
        if not self.end:
            self.cond.acquire()
            self.log.info("Stopping backup process...")

            self.end = True

            if self.creatingBackup:
                self.log.warning("Waiting for backup!")
            else:
                self.cond.notify()

            self.cond.release()

            self.process.join()
            self.log.ok("Backup process stopped!")

    def backupProcess(self):
        self.log.ok(
            "Initialized Backup process at \"{}\"".format(self.mcFolder))
        while not self.end:
            self.cond.acquire()
            self.cond.wait(self.delay)

            if not self.end or self.backupOkExit:
                self.creatingBackup = True
                nBackups = len(os.listdir(self.backupFolder))

                if nBackups > self.maxBackups:
                    self.log.warning("Achieved max number os backups!")
                    self.deleteBackup()

                self.createBackup()
                self.creatingBackup = False

            self.cond.release()

    def deleteBackup(self):
        backups = os.listdir(self.backupFolder)
        backups.sort()
        self.log.info("Deleting oldest backup: \"{}\"".format(backups[0]))
        os.remove("{}/{}".format(self.backupFolder, backups[0]))
        self.log.ok("Deleted oldest backup!")

    def createBackup(self):
        name = datetime.now().strftime(format="%Y-%m-%d_%H-%M-%S")
        backupFile = "{}/{}.tar.gz".format(self.backupFolder, name)
        self.log.info("Creating backup: \"{}\"".format(backupFile))
        with tarfile.open(backupFile, "w:gz") as tar:
            tar.add(self.mcFolder, arcname=os.path.basename(self.mcFolder))
        self.log.ok("Backup created!")


if __name__ == "__main__":
    b = mcBackup(mcFolder="/tmp/world", backupFolder="/tmp/backup",
                 maxBackups=10, delay=0.05, backupOnExit=True, verbose=True)

    if not os.path.isdir("/tmp/world"):
        os.mkdir("/tmp/world")
        os.system("touch /tmp/world/mundo.txt")

    if not os.path.isdir("/tmp/backup"):
        os.mkdir("/tmp/backup")
    else:
        os.system("rm /tmp/backup/*")

    b.start()
    input()
    b.stop()
