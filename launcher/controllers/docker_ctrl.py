import docker
import json
import os
import re
import uuid
import time

from sys import platform
from PySide2.QtCore import QObject
from threading import Thread
from datetime import datetime


class DockerController(QObject):
    def __init__(self, model, view, ctrl, app_root):
        super().__init__()

        self.model = model
        self.main_view = view
        self.main_ctrl = ctrl
        self.app_root = app_root
        self.config_root = os.path.join(self.app_root, "configs")

        # Initialize the client to communicate with the Docker daemon
        self.client = docker.from_env()

        if platform == "linux" or platform == "linux2":
            self.api_client = docker.APIClient(base_url="unix://var/run/docker.sock")
        elif platform == "win32":
            self.api_client = docker.APIClient(base_url="tcp://localhost:2375")
        elif platform == "darwin":
            self.api_client = docker.APIClient(base_url="unix://var/run/docker.sock")

        # Synchronize the record data
        self.sync_record()

    def sync_record(self):
        try:
            container_lst = self.client.containers.list(all=True)
            name_lst = []

            for container in container_lst:
                if "paulcccccch/robustar:" in str(container.image):
                    name_lst.append(container.name)

        except docker.errors.APIError as api_error:
            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser,
                "Unexpected error encountered during record synchronization. "
                "See more in <i>Details</i> page",
                level="error",
            )
            self.main_ctrl.print_message(
                self.main_view.ui.detail_text_browser, str(api_error), level="error"
            )

        new_match_dict = {}
        with open(os.path.join(self.config_root, "config_record.json"), "r") as f:
            match_dict = json.load(f)
            for name in match_dict.keys():
                if name in name_lst:
                    new_match_dict[name] = match_dict[name]
                else:
                    config_file = match_dict[name]
                    os.remove(config_file)
        with open(os.path.join(self.config_root, "config_record.json"), "w") as f:
            json.dump(new_match_dict, f)

    def is_invalid_selection(self):
        items = self.main_ctrl.get_item_from_list_widgets()
        if len(items) == 0:
            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser, "Please select a container first"
            )
            return 1
        else:
            item = items[0]
            self.model.temp_name = item.text()
            return self.no_container_with_name(self.model.temp_name)

    def no_container_with_name(self, name):
        try:
            self.model.container = self.client.containers.get(name)
            return 0
        except docker.errors.NotFound:
            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser,
                "Can not find {}. Refresh <i>Manage</i> page "
                "to check the latest information".format(self.model.temp_name),
            )
            return 1
        except docker.errors.APIError as api_error:
            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser,
                "Unexpected error encountered. See more in <i>Details</i> page",
                level="error",
            )
            self.main_ctrl.print_message(
                self.main_view.ui.detail_text_browser, str(api_error), level="error"
            )
            return 1

    def create_server(self):
        self.model.temp_name = self.model.profile["name"]
        self.model.temp_image = self.model.profile["image"]
        self.model.temp_port = self.model.profile["port"]

        image = "paulcccccch/robustar:" + self.model.profile["image"]

        # save backend relevant configs in a json file
        config = {
            "device": self.model.device,
            "image_size": int(self.model.size),
            "image_padding": self.model.pad,
            "num_classes": int(self.model.cls),
            "port": int(self.model.port),
        }

        config_file = os.path.join(self.config_root, f"config_{uuid.uuid4().hex}.json")
        with open(config_file, "w") as f:
            json.dump(config, f)

        # Store the (container - config file) mapping
        with open(os.path.join(self.config_root, "config_record.json"), "r") as f:
            match_dict = json.load(f)
        with open(os.path.join(self.config_root, "config_record.json"), "w") as f:
            match_dict[self.model.profile["name"]] = config_file
            json.dump(match_dict, f)

        try:
            if "cuda" in self.model.device:
                self.create_new_cuda_server(image, config_file)
            elif "cpu" in self.model.device:
                self.create_new_cpu_server(image, config_file)

            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser,
                "Running {}".format(self.model.temp_image),
            )
            self.main_ctrl.update_success_view()

            self.print_log(self.model.container)

        except docker.errors.APIError as api_error:

            if "port is already allocated" in str(
                api_error
            ) or "Ports are not available" in str(api_error):
                self.main_ctrl.add_item(
                    self.main_view.ui.create_list_widget, self.model.temp_name
                )
                self.main_ctrl.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "{} is created but fails to run "
                    "because the port is "
                    "not available."
                    " See more in <i>Details</i> page".format(self.model.temp_name),
                )
                self.main_ctrl.print_message(
                    self.main_view.ui.detail_text_browser, str(api_error)
                )

            elif (
                "You have to remove (or rename) that container to be able to reuse that name"
                in str(api_error)
            ):
                self.main_ctrl.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "{} can not be created because the "
                    "name is already in use by "
                    "another container."
                    " See more in <i>Details</i> page".format(self.model.temp_name),
                )
                self.main_ctrl.print_message(
                    self.main_view.ui.detail_text_browser, str(api_error)
                )
            else:
                self.main_ctrl.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "Unexpected error encountered. See more in <i>Details</i> page",
                    level="error",
                )
                self.main_ctrl.print_message(
                    self.main_view.ui.detail_text_browser, str(api_error), level="error"
                )
                with open(
                    os.path.join(self.config_root, "config_record.json"), "r"
                ) as f:
                    match_dict = json.load(f)
                with open(
                    os.path.join(self.config_root, "config_record.json"), "w"
                ) as f:
                    config_file = match_dict.pop(self.model.profile["name"])
                    os.remove(config_file)
                    json.dump(match_dict, f)

    def create_new_cpu_server(self, image, config_file):
        self.download_image(image)

        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile["name"],
            ports={"80/tcp": ("127.0.0.1", int(self.model.profile["port"]))},
            mounts=[
                docker.types.Mount(
                    target="/Robustar2/dataset/train",
                    source=get_system_path(self.model.profile["train_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/dataset/validation",
                    source=get_system_path(self.model.profile["val_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/dataset/test",
                    source=get_system_path(self.model.profile["test_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/dataset/paired",
                    source=get_system_path(self.model.profile["paired_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/influence_images",
                    source=get_system_path(self.model.profile["inf_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/generated",
                    source=get_system_path(self.model.profile["out_path"]),
                    type="bind",
                ),
            ],
            volumes=[get_system_path(config_file) + ":/Robustar2/configs.json"],
        )

    def create_new_cuda_server(self, image, config_file):
        self.download_image(image)

        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile["name"],
            ports={"80/tcp": ("127.0.0.1", int(self.model.profile["port"]))},
            mounts=[
                docker.types.Mount(
                    target="/Robustar2/dataset/train",
                    source=get_system_path(self.model.profile["train_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/dataset/validation",
                    source=get_system_path(self.model.profile["val_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/dataset/test",
                    source=get_system_path(self.model.profile["test_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/dataset/paired",
                    source=get_system_path(self.model.profile["paired_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/influence_images",
                    source=get_system_path(self.model.profile["inf_path"]),
                    type="bind",
                ),
                docker.types.Mount(
                    target="/Robustar2/generated",
                    source=get_system_path(self.model.profile["out_path"]),
                    type="bind",
                ),
            ],
            volumes=[config_file + ":/Robustar2/configs.json"],
            # Set the device_requests parm
            device_requests=[
                docker.types.DeviceRequest(
                    counts=-1,
                    device_ids=[self.model.device.split(":")[1]],
                    capabilities=[["gpu"]],
                )
            ],
        )

    def start_server(self):
        if self.is_invalid_selection():
            return
        else:
            try:
                if self.model.container.status == "exited":
                    self.model.container.restart()
                    self.main_ctrl.update_success_view()
                    self.main_ctrl.remove_item(
                        self.main_view.ui.exit_list_widget, self.model.temp_name
                    )

                    self.print_log(self.model.container)

                elif self.model.container.status == "created":
                    self.model.container.start()
                    self.main_ctrl.update_success_view()
                    self.main_ctrl.remove_item(
                        self.main_view.ui.create_list_widget, self.model.temp_name
                    )

                    self.print_log(self.model.container)

                elif self.model.container.status == "running":
                    self.main_ctrl.print_message(
                        self.main_view.ui.prompt_text_browser,
                        "{} is running".format(self.model.temp_name),
                    )

                else:
                    self.main_ctrl.print_message(
                        self.main_view.ui.prompt_text_browser,
                        "Illegal container status encountered",
                        level="error",
                    )
            except docker.errors.APIError as api_error:
                if "port is already allocated" in str(
                    api_error
                ) or "Ports are not available" in str(api_error):
                    self.main_ctrl.print_message(
                        self.main_view.ui.prompt_text_browser,
                        "{} fails to run "
                        "because the port is "
                        "not available."
                        " See more in <i>Details</i> page".format(self.model.temp_name),
                    )
                    self.main_ctrl.print_message(
                        self.main_view.ui.detail_text_browser, str(api_error)
                    )

                else:
                    self.main_ctrl.print_message(
                        self.main_view.ui.prompt_text_browser,
                        "Unexpected error encountered. See more in <i>Details</i> page",
                        level="error",
                    )
                    self.main_ctrl.print_message(
                        self.main_view.ui.detail_text_browser,
                        str(api_error),
                        level="error",
                    )

    def stop_server(self):
        if self.is_invalid_selection():
            return
        try:
            if self.model.container.status == "exited":
                self.main_ctrl.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "{} has already stopped".format(self.model.temp_name),
                )

            elif self.model.container.status == "created":
                self.main_ctrl.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "{} is not running".format(self.model.temp_name),
                )

            elif self.model.container.status == "running":
                self.model.container.stop()
                self.main_ctrl.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "{} is now stopped".format(self.model.temp_name),
                )
                self.main_ctrl.add_item(
                    self.main_view.ui.exit_list_widget, self.model.temp_name
                )
                self.main_ctrl.remove_item(
                    self.main_view.ui.run_list_widget, self.model.temp_name
                )

            else:
                self.main_ctrl.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "Illegal container status encountered",
                    level="error",
                )
        except docker.errors.APIError as api_error:
            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser,
                "Unexpected error encountered. See more in <i>Details</i> page",
                level="error",
            )
            self.main_ctrl.print_message(
                self.main_view.ui.detail_text_browser, str(api_error), level="error"
            )

    def delete_server(self):
        if self.is_invalid_selection():
            return
        try:
            if (
                self.model.container.status == "running"
                or self.model.container.status == "created"
                or self.model.container.status == "exited"
            ):
                self.model.container.remove()
                self.main_ctrl.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "{} removed".format(self.model.temp_name),
                )

                if self.model.container.status == "running":
                    self.main_ctrl.remove_item(
                        self.main_view.ui.run_list_widget, self.model.temp_name
                    )
                elif self.model.container.status == "created":
                    self.main_ctrl.remove_item(
                        self.main_view.ui.create_list_widget, self.model.temp_name
                    )
                elif self.model.container.status == "exited":
                    self.main_ctrl.remove_item(
                        self.main_view.ui.exit_list_widget, self.model.temp_name
                    )

                with open(
                    os.path.join(self.config_root, "config_record.json"), "r"
                ) as f:
                    match_dict = json.load(f)
                with open(
                    os.path.join(self.config_root, "config_record.json"), "w"
                ) as f:
                    config_file = match_dict.pop(self.model.temp_name)
                    os.remove(config_file)
                    json.dump(match_dict, f)
            else:
                self.main_ctrl.print_message(
                    self.main_view.ui.prompt_text_browser,
                    "Illegal container status encountered",
                    level="error",
                )
        except docker.errors.APIError as api_error:
            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser,
                "Unexpected error encountered. See more in <i>Details</i> page",
                level="error",
            )
            self.main_ctrl.print_message(
                self.main_view.ui.detail_text_browser, str(api_error), level="error"
            )

    def refresh_server(self):
        for list_widget in self.main_view.list_widget_lst:
            list_widget.clear()

        try:
            container_lst = self.client.containers.list(all=True)

            for container in container_lst:
                if "paulcccccch/robustar:" in str(container.image):
                    if container.status == "running":
                        self.main_ctrl.add_item(
                            self.main_view.ui.run_list_widget, container.name
                        )
                        self.print_log(container)
                    elif container.status == "exited":
                        self.main_ctrl.add_item(
                            self.main_view.ui.exit_list_widget, container.name
                        )
                    elif container.status == "created":
                        self.main_ctrl.add_item(
                            self.main_view.ui.create_list_widget, container.name
                        )
                    else:
                        self.main_ctrl.print_message(
                            self.main_view.ui.prompt_text_browser,
                            "Illegal container status encountered",
                            level="error",
                        )
        except docker.errors.APIError as api_error:
            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser,
                "Unexpected error encountered. See more in <i>Details</i> page",
                level="error",
            )
            self.main_ctrl.print_message(
                self.main_view.ui.detail_text_browser, str(api_error), level="error"
            )

    def download_image(self, image):
        image_lst = [x.tags[0] for x in self.client.images.list() if x.tags != []]
        if image not in image_lst:
            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser,
                f"Downloading {image}. See more in <i>Details</i> page",
            )
            repo, tag = image.split(":")
            for line in self.api_client.pull(
                repository=repo, tag=tag, stream=True, decode=True
            ):
                self.main_ctrl.print_message(
                    self.main_view.ui.detail_text_browser, str(line)
                )
            self.main_ctrl.print_message(
                self.main_view.ui.prompt_text_browser, f"Downloaded {image}"
            )

    def print_log(self, container):
        def func(ct):
            # Get the logs since current utc time as an iterator
            cur_time = datetime.utcnow()
            logs = ct.logs(stream=True, since=cur_time)

            # Get the name and port setting
            name = ct.name
            with open(os.path.join(self.config_root, "config_record.json"), "r") as f:
                match_dict = json.load(f)
                config_file = match_dict[name]
            with open(config_file) as f:
                config = json.load(f)
                port = config["port"]

            # Print the logs until the container is stopped
            try:
                while True:
                    log = next(logs).decode("utf-8")

                    # Remove the color of log
                    log = re.sub(".\[\d+m", "", log)

                    # Add the name, port and timestamp information
                    current_time = time.strftime("%H:%M:%S", time.localtime())
                    log = (
                        current_time
                        + " - - "
                        + f"{name}({port}) - - "
                        + log[: log.find(" - -")]
                        + log[log.find(" - -") :]
                    )

                    self.main_ctrl.print_message(
                        self.main_view.ui.log_text_browser, log, timestamp=False
                    )
            except StopIteration:
                return

        t = Thread(target=func, args=(container,), daemon=True)
        t.start()


# Change path input by the user to system path
def get_system_path(user_path):
    return str(os.path.normpath(user_path))
