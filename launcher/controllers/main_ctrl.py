import requests
import docker
import os
import json
import time

from PySide2.QtCore import QObject, Qt
from PySide2.QtWidgets import QFileDialog
from threading import Thread


class MainController(QObject):
    def __init__(self):
        super().__init__()

        self.popup_view = None
        self.main_view = None

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
            self.docker_ctrl = DockerController(self.model, self.main_view, self)
            self.docker_ctrl.refresh_server()
            self.main_view.show()
        except requests.RequestException as e:
            self.popup_view.ui.warning_label.setText(
                f"Failed to fetch image versions online!\nPlease check your network!"
            )
            self.popup_view.ui.exception_label.setText(str(e))
            self.popup_view.show()
        except docker.errors.DockerException as e:
            self.popup_view.ui.warning_label.setText(
                "Docker is not running!\nPlease start Docker first!"
            )
            self.popup_view.ui.exception_label.setText(str(e))
            self.popup_view.show()

    # Slot functions to change the model
    def set_m_name(self):
        self.model.name = self.main_view.ui.name_line_edit.text()

    def set_m_image(self):
        self.model.image = self.main_view.ui.image_combo_box.currentText()

    def set_m_port(self):
        self.model.port = self.main_view.ui.port_line_edit.text()

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

    def set_m_out_path(self):
        path = QFileDialog.getExistingDirectory(
            self.main_view, "Choose Output Folder Path", self.model.cwd
        )
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.out_path = path

    def set_m_ckpt_path(self):
        path = QFileDialog.getExistingDirectory(
            self.main_view, "Choose Checkpoints Path", self.model.cwd
        )
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.ckpt_path = path

        self.init_weights()

    def set_m_inf_path(self):
        path = QFileDialog.getExistingDirectory(
            self.main_view, "Choose Influence Result Path", self.model.cwd
        )
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.inf_path = path

    def set_m_arch(self):
        self.model.arch = self.main_view.ui.arch_combo_box.currentText()

    def set_m_pretrain(self):
        if self.main_view.ui.pretrain_check_box.isChecked():
            self.model.pretrain = "True"
        else:
            self.model.pretrain = "False"

    def set_m_weight(self):
        self.model.weight = self.main_view.ui.weight_combo_box.currentText()

    def set_m_device(self):
        self.model.device = self.main_view.ui.device_line_edit.text()

    def set_m_shuffle(self):
        if self.main_view.ui.shuffle_check_box.isChecked():
            self.model.shuffle = "True"
        else:
            self.model.shuffle = "False"

    def set_m_batch(self):
        self.model.batch = self.main_view.ui.batch_line_edit.text()

    def set_m_worker(self):
        self.model.worker = self.main_view.ui.worker_line_edit.text()

    def set_m_size(self):
        self.model.size = self.main_view.ui.size_line_edit.text()

    def set_m_pad(self):
        self.model.pad = self.main_view.ui.pad_combo_box.currentText()

    def set_m_cls(self):
        self.model.cls = self.main_view.ui.cls_line_edit.text()

    def load_profile(self):
        path, _ = QFileDialog.getOpenFileName(
            self.main_view,
            "Load Profile",
            self.model.cwd,
            "JSON Files (*.json);;All Files (*)",
        )
        self.model.cwd = os.path.dirname(path)
        try:
            with open(path, "r") as f:
                self.model.profile = json.load(f)
        except FileNotFoundError:
            print("Load path not found")

    def save_profile(self):
        path, _ = QFileDialog.getSaveFileName(
            self.main_view,
            "Save Profile",
            self.model.cwd,
            "JSON Files (*.json);;All Files (*)",
        )
        self.model.cwd = os.path.dirname(path)
        try:
            with open(path, "w") as f:
                json.dump(self.model.profile, f)
        except FileNotFoundError:
            print("The dialog is closed")

    def start_server(self):
        if self.main_view.ui.cm_tab_widget.currentIndex() == 0 and self.check_miss_input():
            return
        else:
            t = ServerOperationThread(target=self.docker_ctrl.start_server, ctrl=self)
            t.start()

    def stop_server(self):
        if self.main_view.ui.cm_tab_widget.currentIndex() == 0:
            self.print_message(
                self.main_view.ui.prompt_text_browser,
                "Please select a container on Manage Tab Page."),
            return
        t = ServerOperationThread(target=self.docker_ctrl.stop_server, ctrl=self)
        t.start()

    def delete_server(self):
        if self.main_view.ui.cm_tab_widget.currentIndex() == 0:
            self.print_message(
                self.main_view.ui.prompt_text_browser,
                "Please select a container on Manage Tab Page."),
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

    def set_v_train_path(self, val):
        self.main_view.ui.train_line_edit.setText(val)

    def set_v_val_path(self, val):
        self.main_view.ui.val_line_edit.setText(val)

    def set_v_test_path(self, val):
        self.main_view.ui.test_line_edit.setText(val)

    def set_v_paired_path(self, val):
        self.main_view.ui.paired_line_edit.setText(val)

    def set_v_out_path(self, val):
        self.main_view.ui.out_line_edit.setText(val)

    def set_v_ckpt_path(self, val):
        self.main_view.ui.ckpt_line_edit.setText(val)
        self.init_weights()

    def set_v_inf_path(self, val):
        self.main_view.ui.inf_line_edit.setText(val)

    def set_v_arch(self, val):
        self.main_view.ui.arch_combo_box.setCurrentText(val)

    def set_v_pretrain(self, val):
        if val == "True":
            self.main_view.ui.pretrain_check_box.setChecked(True)
        else:
            self.main_view.ui.pretrain_check_box.setChecked(False)

    def set_v_weight(self, val):
        self.main_view.ui.weight_combo_box.setCurrentText(val)

    def set_v_device(self, val):
        self.main_view.ui.device_line_edit.setText(val)

    def set_v_shuffle(self, val):
        if val == "True":
            self.main_view.ui.shuffle_check_box.setChecked(True)
        else:
            self.main_view.ui.shuffle_check_box.setChecked(False)

    def set_v_batch(self, val):
        self.main_view.ui.batch_line_edit.setText(val)

    def set_v_worker(self, val):
        self.main_view.ui.worker_line_edit.setText(val)

    def set_v_size(self, val):
        self.main_view.ui.size_line_edit.setText(val)

    def set_v_pad(self, val):
        self.main_view.ui.pad_combo_box.setCurrentText(val)

    def set_v_cls(self, val):
        self.main_view.ui.cls_line_edit.setText(val)

    def enable_control(self):
        self.main_view.ui.start_push_button.setEnabled(True)
        self.main_view.ui.stop_push_button.setEnabled(True)
        self.main_view.ui.delete_push_button.setEnabled(True)

    def disable_control(self):
        self.main_view.ui.start_push_button.setEnabled(False)
        self.main_view.ui.stop_push_button.setEnabled(False)
        self.main_view.ui.delete_push_button.setEnabled(False)

    def check_miss_input(self):
        miss_profile_dict = {
            "name": "container name",
            "port": "port",
            "train_path": "train set path",
            "val_path": "validation set path",
            "test_path": "test set path",
            "paired_path": "paired set path",
            "out_path": "output folder path",
            "inf_path": "influence result path",
            "ckpt_path": "check point path",
            "batch": "batch size",
            "worker": "worker number",
            "cls": "class number",
            "size": "image size",
            "device": "device"
        }
        miss_profile_prompt = []

        for profile_name in [
            "name",
            "port",
            "train_path",
            "val_path",
            "test_path",
            "paired_path",
            "out_path",
            "inf_path",
            "ckpt_path",
            "batch",
            "worker",
            "cls",
            "size",
            "device"
        ]:
            if not self.model.profile[profile_name].strip():
                miss_profile_prompt.append(miss_profile_dict[profile_name])

        if len(miss_profile_prompt) != 0:
            self.print_message(
                self.main_view.ui.prompt_text_browser,
                "Please provide {}".format(", ".join(miss_profile_prompt)),
            )
            return 1
        return 0

    def check_wrong_input(self):
        pass

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
        with open(os.path.join(self.docker_ctrl.root, "config_record.json"), "r") as f:
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
    def init_weights(self):
        self.main_view.ui.weight_combo_box.clear()
        self.main_view.ui.weight_combo_box.addItem("None")

        for file in os.listdir(self.model.ckpt_path):
            if file.endswith(".pth") or file.endswith(".pt"):
                self.main_view.ui.weight_combo_box.addItem(file)

        self.model.weight = self.main_view.ui.weight_combo_box.currentText()

    # Other control functions
    @staticmethod
    def print_message(text_browser, message, timestamp=True):
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
        item = items[0]
        row = list_widget.row(item)
        list_widget.takeItem(row)


class ServerOperationThread(Thread):
    def __init__(self, target, ctrl):
        Thread.__init__(self, daemon=True)
        self.func = target
        self.ctrl = ctrl

    def run(self):
        self.ctrl.disable_control()
        self.func()
        self.ctrl.enable_control()
