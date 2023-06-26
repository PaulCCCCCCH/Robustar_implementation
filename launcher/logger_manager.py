import logging
import os
from datetime import datetime


class LoggerManager:
    def __init__(self, app_root):
        self.app_root = app_root

        self.logger_names = ["app", "prompt", "detail", "log"]
        self.formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

        time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.logs_root = os.path.join(self.app_root, "logs", time_str)
        os.makedirs(self.logs_root)

    def init_loggers(self):
        for name in self.logger_names:
            self.create_logger(name)

    def create_logger(self, name):
        handler = logging.FileHandler(os.path.join(self.logs_root, f"{name}.log"))
        handler.setFormatter(self.formatter)

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    # TODO: Ensure no call will be made before the loggers are initialized
    @staticmethod
    def append_log(logger_name, level, msg):
        logger = logging.getLogger(logger_name)
        getattr(logger, level)(msg)
