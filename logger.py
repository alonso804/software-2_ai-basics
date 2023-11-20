# Colors
HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKCYAN = "\033[96m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


class Logger:
    @staticmethod
    def info(msg):
        print(OKCYAN + "[INFO] " + ENDC + str(msg))

    @staticmethod
    def warn(msg):
        print(WARNING + "[WARN] " + ENDC + str(msg))

    @staticmethod
    def error(msg):
        print(FAIL + "[ERROR] " + ENDC + str(msg))

    @staticmethod
    def ok(msg):
        print(OKGREEN + "[OK] " + ENDC + str(msg))

    @staticmethod
    def stopError(msg):
        raise SystemExit(FAIL + "[ERROR] " + ENDC + str(msg))

    @staticmethod
    def stopInfo(msg):
        raise SystemExit(OKCYAN + "[INFO] " + ENDC + str(msg))
