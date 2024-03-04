import requests
import docker
import os
import json
import time
import nvgpu
from logger_manager import LoggerManager
from PySide2.QtCore import QObject, Qt
from PySide2.QtWidgets import QFileDialog
from threading import Thread


class MainController(QObject):
    def __init__(self, app_root):
        super().__init__()

        self.popup_view = None
        self.main_view = None
        self.key_to_prompt = {
            "name": "container name",
            "image": "docker image version",
            "port": "port",
            "device": "device",
            "cls": "class number",
            "size": "image size",
            "pad": "padding",
            "train_path": "train set path",
            "val_path": "validation set path",
            "test_path": "test set path",
            "paired_path": "paired set path",
            "inf_path": "influence result path",
            "out_path": "output folder path",
        }

        self.app_root = app_root

    def set_model(self, model):
        self.model = model

    def set_main_view(self, view):
        self.main_view = view

    def set_popup_view(self, view):
        self.popup_view = view

    def init(self):
        from controllers.docker_ctrl import DockerController

        try:
            self.init_images()
            self.init_devices()
            self.docker_ctrl = DockerController(
                self.model, self.main_view, self, self.app_root
            )
            self.docker_ctrl.refresh_server()
            self.main_view.show()
        except requests.RequestException as e:
            text = f"Failed to fetch image versions online!\nPlease check your network!"
            self.popup_view.ui.warning_label.setText(text)
            LoggerManager.append_log("prompt", "warning", text)
            self.popup_view.ui.exception_label.setText(str(e))
            LoggerManager.append_log("detail", "warning", str(e))
            self.popup_view.show()
        except docker.errors.DockerException as e:
            text = "Docker is not running or running properly!\n"
            self.popup_view.ui.warning_label.setText(text)
            LoggerManager.append_log("prompt", "warning", text)
            self.popup_view.ui.exception_label.setText(str(e))
            LoggerManager.append_log("detail", "warning", str(e))
            self.popup_view.show()

    # Slot functions to change the model
    def set_m_name(self):
        self.model.name = self.main_view.ui.name_line_edit.text()

    def set_m_image(self):
        self.model.image = self.main_view.ui.image_combo_box.currentText()

    def set_m_port(self):
        self.model.port = self.main_view.ui.port_line_edit.text()

    def set_m_device(self):
        self.model.device = self.main_view.ui.device_combo_box.currentText()

    def set_m_cls(self):
        self.model.cls = self.main_view.ui.cls_line_edit.text()

    def set_m_size(self):
        self.model.size = self.main_view.ui.size_line_edit.text()

    def set_m_pad(self):
        # To align with the backend
        match_dict = {"short side": "short_side", "none": "none"}
        self.model.pad = match_dict[self.main_view.ui.pad_combo_box.currentText()]

    def set_m_train_path(self):
        path = QFileDialog.getExistingDirectory(
            self.main_view, "Choose Train Set Path", self.model.cwd
        )
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.train_path = path

    def set_m_val_path(self):
        path = QFileDialog.getExistingDirectory(
            self.main_view, "Choose Validation Set Path", self.model.cwd
        )
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.val_path = path

    def set_m_test_path(self):
        path = QFileDialog.getExistingDirectory(
            self.main_view, "Choose Test Set Path", self.model.cwd
        )
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.test_path = path

    def set_m_paired_path(self):
        path = QFileDialog.getExistingDirectory(
            self.main_view, "Choose Paired Set Path", self.model.cwd
        )
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.paired_path = path

    def set_m_inf_path(self):
        path = QFileDialog.getExistingDirectory(
            self.main_view, "Choose Influence Result Path", self.model.cwd
        )
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.inf_path = path

    def set_m_out_path(self):
        path = QFileDialog.getExistingDirectory(
            self.main_view, "Choose Output Folder Path", self.model.cwd
        )
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.out_path = path

    def load_profile(self):
        path, _ = QFileDialog.getOpenFileName(
            self.main_view,
            "Load Profile",
            self.model.cwd,
            "JSON Files (*.json);;All Files (*)",
        )

        if path.strip():
            self.model.cwd = os.path.dirname(path)
            try:
                with open(path, "r") as f:
                    self.model.profile = json.load(f)
            except FileNotFoundError:
                self.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "Failed to find the profile file.",
                    level="warning",
                )

    def save_profile(self):
        path, _ = QFileDialog.getSaveFileName(
            self.main_view,
            "Save Profile",
            self.model.cwd,
            "JSON Files (*.json);;All Files (*)",
        )

        if path.strip():
            self.model.cwd = os.path.dirname(path)
            with open(path, "w") as f:
                json.dump(self.model.profile, f)

    def create_server(self):
        if self.check_miss_input() or self.check_wrong_input():
            return
        else:
            t = ServerOperationThread(target=self.docker_ctrl.create_server, ctrl=self)
            t.start()

    def start_server(self):
        t = ServerOperationThread(target=self.docker_ctrl.start_server, ctrl=self)
        t.start()

    def stop_server(self):
        if self.main_view.ui.cm_tab_widget.currentIndex() == 0:
            self.print_message(
                self.main_view.ui.prompt_text_browser,
                "Please select a container on Manage Tab Page.",
            ),
            return
        t = ServerOperationThread(target=self.docker_ctrl.stop_server, ctrl=self)
        t.start()

    def delete_server(self):
        if self.main_view.ui.cm_tab_widget.currentIndex() == 0:
            self.print_message(
                self.main_view.ui.prompt_text_browser,
                "Please select a container on Manage Tab Page.",
            ),
            return
        t = ServerOperationThread(target=self.docker_ctrl.delete_server, ctrl=self)
        t.start()

    def refresh_server(self):
        t = Thread(target=self.docker_ctrl.refresh_server)
        t.start()

    # Slot functions to change the view
    def set_v_name(self, val):
        self.main_view.ui.name_line_edit.setText(val)

    def set_v_image(self, val):
        self.main_view.ui.image_combo_box.setCurrentText(val)

    def set_v_port(self, val):
        self.main_view.ui.port_line_edit.setText(val)

    def set_v_device(self, val):
        self.main_view.ui.device_combo_box.setCurrentText(val)

    def set_v_cls(self, val):
        self.main_view.ui.cls_line_edit.setText(val)

    def set_v_size(self, val):
        self.main_view.ui.size_line_edit.setText(val)

    def set_v_pad(self, val):
        # To align with the backend
        match_dict = {"short_side": "short side", "none": "none"}
        self.main_view.ui.pad_combo_box.setCurrentText(match_dict[val])

    def set_v_train_path(self, val):
        self.main_view.ui.train_line_edit.setText(val)

    def set_v_val_path(self, val):
        self.main_view.ui.val_line_edit.setText(val)

    def set_v_test_path(self, val):
        self.main_view.ui.test_line_edit.setText(val)

    def set_v_paired_path(self, val):
        self.main_view.ui.paired_line_edit.setText(val)

    def set_v_inf_path(self, val):
        self.main_view.ui.inf_line_edit.setText(val)

    def set_v_out_path(self, val):
        self.main_view.ui.out_line_edit.setText(val)

    def enable_control(self):
        self.main_view.ui.create_push_button.setEnabled(True)
        self.main_view.ui.start_push_button.setEnabled(True)
        self.main_view.ui.stop_push_button.setEnabled(True)
        self.main_view.ui.delete_push_button.setEnabled(True)
        self.main_view.ui.refresh_push_button.setEnabled(True)

    def disable_control(self):
        self.main_view.ui.create_push_button.setEnabled(False)
        self.main_view.ui.start_push_button.setEnabled(False)
        self.main_view.ui.stop_push_button.setEnabled(False)
        self.main_view.ui.delete_push_button.setEnabled(False)
        self.main_view.ui.refresh_push_button.setEnabled(False)

    def check_miss_input(self):
        miss_input_prompt = []

        for key in self.key_to_prompt:
            if not self.model.profile[key].strip():
                miss_input_prompt.append(self.key_to_prompt[key])

        if len(miss_input_prompt) != 0:
            self.print_message(
                self.main_view.ui.prompt_text_browser,
                "Please provide {}".format(", ".join(miss_input_prompt)),
            )
            return 1
        return 0

    def check_wrong_input(self):
        wrong_input_prompt = []

        for key in ["port", "cls", "size"]:
            if not self.model.profile[key].isdigit():
                wrong_input_prompt.append(self.key_to_prompt[key])

        if len(wrong_input_prompt) != 0:
            self.print_message(
                self.main_view.ui.prompt_text_browser,
                "The input type of {} should be integer".format(
                    ", ".join(wrong_input_prompt)
                ),
            )
            return 1
        return 0

    def get_item_from_list_widgets(self):
        return (
            self.main_view.ui.run_list_widget.selectedItems()
            if len(self.main_view.ui.run_list_widget.selectedItems()) > 0
            else self.main_view.ui.exit_list_widget.selectedItems()
            if len(self.main_view.ui.exit_list_widget.selectedItems()) > 0
            else self.main_view.ui.create_list_widget.selectedItems()
            if len(self.main_view.ui.create_list_widget.selectedItems()) > 0
            else []
        )

    def update_success_view(self):
        with open(
            os.path.join(self.docker_ctrl.config_root, "config_record.json"), "r"
        ) as f:
            match_dict = json.load(f)
            file_name = match_dict[self.model.temp_name]
        with open(file_name) as f:
            config = json.load(f)
            port = config["port"]

        self.print_message(
            self.main_view.ui.prompt_text_browser,
            "{} is available at http://localhost:{}".format(self.model.temp_name, port),
        )
        self.add_item(self.main_view.ui.run_list_widget, self.model.temp_name)

    # Fetch the docker image versions to add to the image version combobox and initiate model's image version
    def init_images(self):
        res = requests.get(
            "https://registry.hub.docker.com/v2/repositories/paulcccccch/robustar/tags?page_size=1024",
            timeout=3,
        )

        for item in res.json()["results"]:
            self.main_view.ui.image_combo_box.addItem(item["name"])
        self.model.image = self.main_view.ui.image_combo_box.currentText()

    # Scan the checkpoint directory to add checkpoint files to the weight file combobox and initiates model's weight file
    def init_ckpts(self):
        self.main_view.ui.weight_combo_box.clear()
        self.main_view.ui.weight_combo_box.addItem("None")

        for file in os.listdir(self.model.ckpt_path):
            if file.endswith(".pth") or file.endswith(".pt"):
                self.main_view.ui.weight_combo_box.addItem(file)

        self.model.weight = self.main_view.ui.weight_combo_box.currentText()

    def init_devices(self):
        try:
            for gpu_info in nvgpu.gpu_info():
                if gpu_info["mem_used_percent"] < 100:
                    self.main_view.ui.device_combo_box.addItem(
                        f"cuda:{gpu_info['index']}"
                    )
        except Exception as e:
            print(e)
            LoggerManager.append_log("app", "info", e)

    # Other control functions
    @staticmethod
    def print_message(text_browser, message, level="info", timestamp=True):
        logger_name = text_browser.objectName().split("_")[0]
        LoggerManager.append_log(logger_name, level, message)

        if timestamp is True:
            current_time = time.strftime("%H:%M:%S", time.localtime())
            message = current_time + " - - " + message + "\n"
        text_browser.append(message)
        text_browser.verticalScrollBar().setValue(
            text_browser.verticalScrollBar().maximum()
        )

    @staticmethod
    def add_item(list_widget, name):
        list_widget.addItem(name)

    @staticmethod
    def remove_item(list_widget, name):
        items = list_widget.findItems(name, Qt.MatchExactly)
        if len(items):
            item = items[0]
            row = list_widget.row(item)
            list_widget.takeItem(row)
        else:
            LoggerManager.append_log(
                "app", "info", "The container to be removed changed its state"
            )
            return


class ServerOperationThread(Thread):
    def __init__(self, target, ctrl):
        Thread.__init__(self, daemon=True)
        self.func = target
        self.ctrl = ctrl

    def run(self):
        self.ctrl.disable_control()
        self.func()
        self.ctrl.enable_control()
