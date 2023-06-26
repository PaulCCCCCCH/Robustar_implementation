import os
import sys
import ctypes
import json
import traceback
import threading
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

        sys.excepthook = lambda cls, excp, tb: App.sys_except_hook(self, cls, excp, tb)
        threading.excepthook = lambda args: App.thread_except_hook(self, args)

        self.main_ctrl = MainController(self.app_root)

        self.model = Model(self.main_ctrl)

        self.main_view = MainView(self.main_ctrl)
        self.popup_view = PopupView()

        self.main_ctrl.set_model(self.model)
        self.main_ctrl.set_main_view(self.main_view)
        self.main_ctrl.set_popup_view(self.popup_view)

        self.main_ctrl.init()

    def sys_except_hook(self, cls, excp, tb):
        tb = '\n\t\t'.join([x.strip() for x in traceback.format_tb(tb)])
        LoggerManager.append_log("app", "critical",
                                 f'{cls.__name__}: {excp}\n\t Traceback:\n\t\t {tb}')
        sys.__excepthook__(cls, excp, tb)
        self.main_ctrl.print_message(
            self.main_view.ui.prompt_text_browser,
            f"An unexpected error occurred. You may close the launcher and restart it.\n"
            f"More information can be found in {os.path.join(self.logger_manager.logs_root, 'app.log')}",
            level="critical"
        )

    def thread_except_hook(self, args):
        tb = '\n\t\t'.join([x.strip() for x in traceback.format_tb(args.exc_traceback)])
        LoggerManager.append_log("app", "critical",
                                 f'{args.exc_type.__name__}: {args.exc_value}\n\t Traceback:\n\t\t {tb}')
        sys.__excepthook__(args.exc_type, args.exc_value, args.exc_traceback)
        self.main_ctrl.print_message(
            self.main_view.ui.prompt_text_browser,
            f"An unexpected error occurred. You may close the launcher and restart it.\n"
            f"More information can be found in {os.path.join(self.logger_manager.logs_root, 'app.log')}",
            level="critical"
        )


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
