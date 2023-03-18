import os
import sys
import ctypes
import json
import traceback
from sys import platform
from PySide2.QtWidgets import QApplication
from logger_manager import LoggerManager
from model.model import Model
from controllers.main_ctrl import MainController
from views.main_view import MainView
from views.popup_view import PopupView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        home_dir = os.path.expanduser("~")
        if platform == "linux" or platform == "linux2":
            self.app_root = os.path.join(home_dir, ".RobustarLauncher")
        elif platform == "win32":
            self.app_root = os.path.join(home_dir, "AppData", "Local", "RobustarLauncher")
        elif platform == "darwin":
            self.app_root = os.path.join(home_dir, "Library", "Application Support", "RobustarLauncher")

        if not os.path.exists(self.app_root):
            os.makedirs(self.app_root)
            os.makedirs(os.path.join(self.app_root, "configs"))
            os.makedirs(os.path.join(self.app_root, "logs"))
            with open(os.path.join(self.app_root, "configs", "config_record.json"), "w") as f:
                json.dump({}, f)

            if platform == "win32":
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ret = ctypes.windll.kernel32.SetFileAttributesW(self.app_root,
                                                                FILE_ATTRIBUTE_HIDDEN)
                if not ret:
                    print("Failed to hide the record folder")

        self.logger_manager = LoggerManager(self.app_root)
        self.logger_manager.init_loggers()

        sys.excepthook = App.except_hook

        self.mainCtrl = MainController(self.app_root)

        self.model = Model(self.mainCtrl)

        self.mainView = MainView(self.mainCtrl)
        self.popupView = PopupView()

        self.mainCtrl.set_model(self.model)
        self.mainCtrl.set_main_view(self.mainView)
        self.mainCtrl.set_popup_view(self.popupView)

        self.mainCtrl.init()

    @staticmethod
    def except_hook(cls, excp, tb):
        LoggerManager.append_log("app", "critical",
                                 f'{cls.__name__}: {excp}\n\t Traceback: {traceback.format_tb(tb)[0].strip()}')
        sys.__excepthook__(cls, excp, tb)


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
