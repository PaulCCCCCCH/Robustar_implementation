import docker
import json
import os
import re
import uuid

from sys import platform
from PySide2.QtCore import QObject
from threading import Thread
from datetime import datetime


class DockerController(QObject):
    def __init__(self, model, view, ctrl):
        super().__init__()

        self.model = model
        self.main_view = view
        self.main_ctrl = ctrl

        # Initialize the client to communicate with the Docker daemon
        self.client = docker.from_env()
        if platform == "linux" or platform == "linux2":
            self.api_client = docker.APIClient(base_url="unix://var/run/docker.sock")
        elif platform == "win32":
            self.api_client = docker.APIClient(base_url="tcp://localhost:2375")

    def get_selection(self, for_start=False):
        if self.main_view.ui.cm_tab_widget.currentIndex() == 0:
            self.model.made_on_create = True
            self.model.temp_name = self.model.profile["name"]
            if for_start is True:
                self.model.temp_image = self.model.profile["image"]
                self.model.temp_port = self.model.profile["port"]
            return self.get_container_by_name(self.model.temp_name, for_start=for_start)
        else:
            self.model.made_on_create = False
            items = self.main_ctrl.get_item_from_list_widgets()
            if len(items) == 0:
                self.model.temp_name = None
                self.model.container = None
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "Please select a container first")
                return 1
            else:
                item = items[0]
                self.model.temp_name = item.text()
                return self.get_container_by_name(self.model.temp_name, for_start=for_start)

    def get_container_by_name(self, name, for_start):
        try:
            self.model.container = self.client.containers.get(name)
            return 0
        except docker.errors.NotFound:
            if self.model.made_on_create and for_start is True:
                self.model.container = None
                return 0
            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "Can not find {}. Refresh <i>Manage</i> page "
                                             "to check the latest information".format(self.model.temp_name))
                return 1
        except docker.errors.APIError as api_error:
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                         "Unexpected error encountered. See more in <i>Details</i> page")
            self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(api_error))
            return 1

    def start_server(self):
        if self.get_selection(for_start=True):
            return
        if self.model.container is None:
            self.start_new_server()
        else:
            self.start_exist_server()

    def start_new_server(self):
        image = "paulcccccch/robustar:" + self.model.profile["image"]

        # save backend relevant configs in a json file
        config = {
            "model_arch": self.model.arch,
            "pre_trained": True if self.model.pretrain == "True" else False,
            "weight_to_load": self.model.weight,
            "device": self.model.device,
            "shuffle": True if self.model.shuffle == "True" else False,
            "batch_size": int(self.model.batch),
            "num_workers": int(self.model.worker),
            "image_size": int(self.model.size),
            "image_padding": self.model.pad,
            "num_classes": int(self.model.cls),
            "port": int(self.model.port)
        }

        # Create folder to store record data
        if not os.path.exists("./RecordData"):
            os.makedirs("./RecordData")

        file_name = f"./RecordData/config_{uuid.uuid4().hex}.json"
        with open(file_name, "w") as f:
            f.write(json.dumps(config))
        config_file = os.path.join(os.getcwd(), file_name)

        # Store the (container - config file) mapping
        if not os.path.exists("./RecordData/config_record.json"):
            match_dict = {}
        else:
            with open("./RecordData/config_record.json", "r") as f:
                match_dict = json.load(f)
        with open("./RecordData/config_record.json", "w") as f:
            match_dict[self.model.profile["name"]] = file_name
            json.dump(match_dict, f)

        try:
            if "cuda" in self.model.device:
                self.start_new_cuda_server(image, config_file)
            elif "cpu" in self.model.device:
                self.start_new_cpu_server(image, config_file)

            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "Running {}".format(
                self.model.temp_image))
            self.main_ctrl.update_success_view()

            self.print_log(self.model.container)

        except docker.errors.APIError as api_error:

            if "port is already allocated" in str(api_error):
                self.main_ctrl.add_item(self.main_view.ui.create_list_widget, self.model.temp_name)
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} is created but fails to run "
                                                                                    "because port is already allocated."
                                                                                    " See more in <i>Details</i> page"
                                             .format(self.model.temp_name))
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(api_error))

            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "Unexpected error encountered. See more in <i>Details</i> page")
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(api_error))
                with open("./RecordData/config_record.json", "r") as f:
                    match_dict = json.load(f)
                with open("./RecordData/config_record.json", "w") as f:
                    file_name = match_dict.pop(self.model.profile["name"])
                    os.remove(file_name)
                    json.dump(match_dict, f)

    def start_new_cpu_server(self, image, config_file):
        self.download_image(image)

        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile["name"],
            ports={
                "80/tcp": (
                    "127.0.0.1", int(self.model.profile["port"]))
            },
            mounts=[
                docker.types.Mount(target="/Robustar2/dataset/train",
                                   source=get_system_path(self.model.profile["train_path"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/dataset/validation",
                                   source=get_system_path(self.model.profile["val_path"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/dataset/test",
                                   source=get_system_path(self.model.profile["test_path"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/influence_images",
                                   source=get_system_path(self.model.profile["inf_path"]),
                                   type="bind"),
                docker.types.Mount(
                    target="/Robustar2/checkpoints",
                    source=get_system_path(self.model.profile["ckpt_path"]),
                    type="bind"),
            ],
            volumes=[
                get_system_path(config_file) + ":/Robustar2/configs.json"]
        )

    def start_new_cuda_server(self, image, config_file):
        self.download_image(image)

        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile["name"],
            ports={
                "80/tcp": (
                    "127.0.0.1", int(self.model.profile["port"]))
            },
            mounts=[
                docker.types.Mount(target="/Robustar2/dataset/train",
                                   source=get_system_path(self.model.profile["train_path"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/dataset/validation",
                                   source=get_system_path(self.model.profile["val_path"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/dataset/test",
                                   source=get_system_path(self.model.profile["test_path"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/influence_images",
                                   source=get_system_path(self.model.profile["inf_path"]),
                                   type="bind"),
                docker.types.Mount(
                    target="/Robustar2/checkpoints",
                    source=get_system_path(self.model.profile["ckpt_path"]),
                    type="bind"),
            ],
            volumes=[
                config_file + ":/Robustar2/configs.json"],

            # Set the device_requests parm
            device_requests=[
                docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])
            ]
        )

    def start_exist_server(self):
        try:
            if self.model.container.status == "exited":
                self.model.container.restart()
                self.main_ctrl.update_success_view()
                self.main_ctrl.remove_item(self.main_view.ui.exit_list_widget, self.model.temp_name)

                self.print_log(self.model.container)

            elif self.model.container.status == "created":
                self.model.container.start()
                self.main_ctrl.update_success_view()
                self.main_ctrl.remove_item(self.main_view.ui.create_list_widget, self.model.temp_name)

                self.print_log(self.model.container)

            elif self.model.container.status == "running":
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} is running".format(
                    self.model.temp_name))

            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "Illegal container status encountered")
        except docker.errors.APIError as api_error:
            if "port is already allocated" in str(api_error):

                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} fails to run because port is "
                                                                                    "already allocated. See more in"
                                                                                    " <i>Details</i> page".format(
                                                                                                self.model.temp_name))
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(api_error))

            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "Unexpected error encountered. See more in <i>Details</i> page")
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(api_error))

    def stop_server(self):
        if self.get_selection():
            return
        try:
            if self.model.container.status == "exited":
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "{} has already stopped".format(self.model.temp_name))

            elif self.model.container.status == "created":
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "{} is not running".format(self.model.temp_name))

            elif self.model.container.status == "running":
                self.model.container.stop()
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "{} is now stopped".format(self.model.temp_name))
                self.main_ctrl.add_item(self.main_view.ui.exit_list_widget, self.model.temp_name)
                self.main_ctrl.remove_item(self.main_view.ui.run_list_widget, self.model.temp_name)

            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "Illegal container status encountered")
        except docker.errors.APIError as api_error:
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                         "Unexpected error encountered. See more in <i>Details</i> page")
            self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(api_error))

    def delete_server(self):
        if self.get_selection():
            return
        try:
            if self.model.container.status == "running" or self.model.container.status == "created" or \
                    self.model.container.status == "exited":
                self.model.container.remove()
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "{} removed".format(self.model.temp_name))

                if self.model.container.status == "running":
                    self.main_ctrl.remove_item(self.main_view.ui.run_list_widget, self.model.temp_name)
                elif self.model.container.status == "created":
                    self.main_ctrl.remove_item(self.main_view.ui.create_list_widget, self.model.temp_name)
                elif self.model.container.status == "exited":
                    self.main_ctrl.remove_item(self.main_view.ui.exit_list_widget, self.model.temp_name)

                with open("./RecordData/config_record.json", "r") as f:
                    match_dict = json.load(f)
                with open("./RecordData/config_record.json", "w") as f:
                    file_name = match_dict.pop(self.model.temp_name)
                    os.remove(file_name)
                    json.dump(match_dict, f)
            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                             "Illegal container status encountered")
        except docker.errors.APIError as api_error:
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                         "Unexpected error encountered. See more in <i>Details</i> page")
            self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(api_error))

    def refresh_server(self):
        for list_widget in self.main_view.list_widget_lst:
            list_widget.clear()

        try:
            container_lst = self.client.containers.list(all=True)

            for container in container_lst:
                if "paulcccccch/robustar:" in str(container.image):
                    if container.status == "running":
                        self.main_ctrl.add_item(self.main_view.ui.run_list_widget, container.name)
                        self.print_log(container)
                    elif container.status == "exited":
                        self.main_ctrl.add_item(self.main_view.ui.exit_list_widget, container.name)
                    elif container.status == "created":
                        self.main_ctrl.add_item(self.main_view.ui.create_list_widget, container.name)
                    else:
                        self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                                     "Illegal container status encountered")
        except docker.errors.APIError as api_error:
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                         "Unexpected error encountered. See more in <i>Details</i> page")
            self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(api_error))

    def download_image(self, image):
        image_lst = [x.tags[0] for x in self.client.images.list() if x.tags != []]
        if image not in image_lst:
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                         f"Downloading {image}. See more in <i>Details</i> page")
            repo, tag = image.split(":")
            for line in self.api_client.pull(repository=repo, tag=tag, stream=True, decode=True):
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(line))
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, f"Downloaded {image}")

    def print_log(self, container):
        def func(ct):
            # Get the logs since current utc time as an iterator
            cur_time = datetime.utcnow()
            logs = ct.logs(stream=True, since=cur_time)

            # Get the name and port setting
            name = ct.name
            with open("./RecordData/config_record.json", "r") as f:
                match_dict = json.load(f)
                file_name = match_dict[name]
            with open(file_name) as f:
                config = json.load(f)
                port = config["port"]

            # Print the logs until the container is stopped
            try:
                while True:
                    log = next(logs).decode("utf-8")

                    # Remove the color of log
                    log = re.sub(".\[\d+m", "", log)

                    # Add the name and port information
                    log = f"{name} - - " + log[:log.find(" - -")] + f":{port}" + log[log.find(" - -"):]

                    self.main_ctrl.print_message(self.main_view.ui.log_text_browser, log, timestamp=False)
            except StopIteration:
                return

        t = Thread(target=func, args=(container,), daemon=True)
        t.start()


# Change path input by the user to system path
def get_system_path(user_path):
    return str(os.path.normpath(user_path))
