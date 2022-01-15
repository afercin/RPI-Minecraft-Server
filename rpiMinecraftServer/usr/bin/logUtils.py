from datetime import datetime
import inspect


class logUtils():
    LOGPATH = "/var/log/product"

    def __init__(self, verbose=False):
        invokeClass = inspect.stack()[1][0].f_locals["self"].__class__.__name__
        self.filename = "{}/{}.log".format(logUtils.LOGPATH, invokeClass)
        self.verbose = verbose
        self.write(
            "◤━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◥", False)

    def dispose(self):
        self.write(
            "◣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◢", False)

    def debug(self, msg):
        self.write("[DEBUG] {}".format(msg))

    def info(self, msg):
        self.write("[INFO] {}".format(msg))
        
    def ok(self, msg):
        self.write("[OK] {}".format(msg))

    def warning(self, msg):
        self.write("[WARNING] {}".format(msg))

    def error(self, msg):
        self.write("[ERROR] {}".format(msg))

    def write(self, msg, date=True):
        f = open(self.filename, "a")
        if date:
            msg = "[{}]{}".format(datetime.now().strftime(
                format="%Y/%m/%d %H:%M:%S"), msg)
            f.write("{}\n".format(msg))
            if self.verbose:
                print(msg)
        else:
            f.write("{}\n".format(msg))
        f.close()
