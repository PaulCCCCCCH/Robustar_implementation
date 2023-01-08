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
            self.model.temp_name = self.model.profile["containerName"]
            if for_start is True:
                self.model.temp_image = self.model.profile["imageVersion"]
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
        image = "paulcccccch/robustar:" + self.model.profile["imageVersion"]

        # save backend relevant configs in a json file
        config = {
            "model_arch": self.model.modelArch,
            "pre_trained": True if self.model.pretrained == "True" else False,
            "weight_to_load": self.model.weightFile,
            "device": self.model.device,
            "shuffle": True if self.model.shuffle == "True" else False,
            "batch_size": int(self.model.batchSize),
            "num_workers": int(self.model.workerNumber),
            "image_size": int(self.model.imgSize),
            "image_padding": self.model.padding,
            "num_classes": int(self.model.classNumber),
            "port": int(self.model.port)
        }

        # Create folder to store record data
        if not os.path.exists("./RecordData"):
            os.makedirs("./RecordData")

        fileName = f"./RecordData/config_{uuid.uuid4().hex}.json"
        with open(fileName, "w") as f:
            f.write(json.dumps(config))
        configFile = os.path.join(os.getcwd(), fileName)

        # Store the (container - config file) matching
        if not os.path.exists("./RecordData/config_record.json"):
            matchDict = {}
        else:
            with open("./RecordData/config_record.json", "r") as f:
                matchDict = json.load(f)
        with open("./RecordData/config_record.json", "w") as f:
            matchDict[self.model.profile["containerName"]] = fileName
            json.dump(matchDict, f)

        try:
            if "cuda" in self.model.device:
                self.startNewCudaServer(image, configFile)
            elif "cpu" in self.model.device:
                self.startNewCpuServer(image, configFile)

            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "Running {}".format(self.model.temp_image))
            self.main_ctrl.updateSucView()

            self.printLog(self.model.container)


        except docker.errors.APIError as apiError:

            if ("port is already allocated" in str(apiError)):

                self.main_ctrl.addItem(self.main_view.ui.create_list_widget, self.model.temp_name)
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} is created but fails to run because port is already allocated. See more in <i>Details</i> page".format(self.model.temp_name))
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(apiError))

            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                            "Unexpected error encountered. See more in <i>Details</i> page")
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(apiError))
                with open("./RecordData/config_record.json", "r") as f:
                    matchDict = json.load(f)
                with open("./RecordData/config_record.json", "w") as f:
                    fileName = matchDict.pop(self.model.profile["containerName"])
                    os.remove(fileName)
                    json.dump(matchDict, f)


    def startNewCpuServer(self, image, configFile):
        self.downloadImage(image)

        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile["containerName"],
            ports={
                "80/tcp": (
                    "127.0.0.1", int(self.model.profile["port"]))
            },
            mounts=[
                docker.types.Mount(target="/Robustar2/dataset/train",
                                   source=getSystemPath(self.model.profile["trainPath"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/dataset/validation",
                                   source=getSystemPath(self.model.profile["validationPath"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/dataset/test",
                                   source=getSystemPath(self.model.profile["testPath"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/influence_images",
                                   source=getSystemPath(self.model.profile["influencePath"]),
                                   type="bind"),
                docker.types.Mount(
                    target="/Robustar2/checkpoints",
                    source=getSystemPath(self.model.profile["checkPointPath"]),
                    type="bind"),
            ],
            volumes=[
                getSystemPath(configFile) + ":/Robustar2/configs.json"]
        )

    def startNewCudaServer(self, image, configFile):
        self.downloadImage(image)

        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile["containerName"],
            ports={
                "80/tcp": (
                    "127.0.0.1", int(self.model.profile["port"]))
            },
            mounts=[
                docker.types.Mount(target="/Robustar2/dataset/train",
                                   source=getSystemPath(self.model.profile["trainPath"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/dataset/validation",
                                   source=getSystemPath(self.model.profile["validationPath"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/dataset/test",
                                   source=getSystemPath(self.model.profile["testPath"]),
                                   type="bind"),
                docker.types.Mount(target="/Robustar2/influence_images",
                                   source=getSystemPath(self.model.profile["influencePath"]),
                                   type="bind"),
                docker.types.Mount(
                    target="/Robustar2/checkpoints",
                    source=getSystemPath(self.model.profile["checkPointPath"]),
                    type="bind"),
            ],
            volumes=[
                configFile + ":/Robustar2/configs.json"],

            # Set the device_requests parm
            device_requests=[
                docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])
            ]
        )

    def start_exist_server(self):
        try:
            if self.model.container.status == "exited":
                self.model.container.restart()
                self.main_ctrl.updateSucView()
                self.main_ctrl.removeItem(self.main_view.ui.exit_list_widget, self.model.temp_name)

                self.printLog(self.model.container)

            elif self.model.container.status == "created":
                self.model.container.start()
                self.main_ctrl.updateSucView()
                self.main_ctrl.removeItem(self.main_view.ui.create_list_widget, self.model.temp_name)

                self.printLog(self.model.container)

            elif self.model.container.status == "running":
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} is running".format(self.model.temp_name))

            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "Illegal container status encountered")
        except docker.errors.APIError as apiError:
            if ("port is already allocated" in str(apiError)):

                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} fails to run because port is already allocated. See more in <i>Details</i> page".format(self.model.temp_name))
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(apiError))

            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                            "Unexpected error encountered. See more in <i>Details</i> page")
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(apiError))

    def stopServer(self):
        if(self.get_selection()):
            return
        try:
            if self.model.container.status == "exited":
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} has already stopped".format(self.model.temp_name))

            elif self.model.container.status == "created":
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} is not running".format(self.model.temp_name))

            elif self.model.container.status == "running":
                self.model.container.stop()
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} is now stopped".format(self.model.temp_name))
                self.main_ctrl.addItem(self.main_view.ui.exit_list_widget, self.model.temp_name)
                self.main_ctrl.removeItem(self.main_view.ui.run_list_widget, self.model.temp_name)

            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                                           "Illegal container status encountered")
        except docker.errors.APIError as apiError:
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                       "Unexpected error encountered. See more in <i>Details</i> page")
            self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(apiError))

    def deleteServer(self):
        if(self.get_selection()):
            return
        try:
            if self.model.container.status == "running" or self.model.container.status == "created" or self.model.container.status == "exited":
                self.model.container.remove()
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, "{} removed".format(self.model.temp_name))

                if(self.model.container.status == "running"):
                    self.main_ctrl.removeItem(self.main_view.ui.run_list_widget, self.model.temp_name)
                elif(self.model.container.status == "created"):
                    self.main_ctrl.removeItem(self.main_view.ui.create_list_widget, self.model.temp_name)
                elif (self.model.container.status == "exited"):
                    self.main_ctrl.removeItem(self.main_view.ui.exit_list_widget, self.model.temp_name)

                with open("./RecordData/config_record.json", "r") as f:
                    matchDict = json.load(f)
                with open("./RecordData/config_record.json", "w") as f:
                    fileName = matchDict.pop(self.model.temp_name)
                    os.remove(fileName)
                    json.dump(matchDict, f)
            else:
                self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                                           "Illegal container status encountered")
        except docker.errors.APIError as apiError:
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                       "Unexpected error encountered. See more in <i>Details</i> page")
            self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(apiError))

    def refreshServers(self):
        for listWidget in self.main_view.list_widget_lst:
            listWidget.clear()

        try:
            containerList = self.client.containers.list(all=True)

            for container in containerList:
                if ("paulcccccch/robustar:" in str(container.image)):
                    if (container.status == "running"):
                        self.main_ctrl.addItem(self.main_view.ui.run_list_widget, container.name)

                        self.printLog(container)
                    elif (container.status == "exited"):
                        self.main_ctrl.addItem(self.main_view.ui.exit_list_widget, container.name)
                    elif (container.status == "created"):
                        self.main_ctrl.addItem(self.main_view.ui.create_list_widget, container.name)
                    else:
                        self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                                                   "Illegal container status encountered")
        except docker.errors.APIError as apiError:
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                       "Unexpected error encountered. See more in <i>Details</i> page")
            self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(apiError))

    def downloadImage(self, image):
        imageList = [x.tags[0] for x in self.client.images.list() if x.tags != []]
        if image not in imageList:
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser,
                                       f"Downloading {image}. See more in <i>Details</i> page")
            repo, tag = image.split(":")
            for line in self.api_client.pull(repository=repo, tag=tag, stream=True, decode=True):
                self.main_ctrl.print_message(self.main_view.ui.detail_text_browser, str(line))
            self.main_ctrl.print_message(self.main_view.ui.prompt_text_browser, f"Downloaded {image}")

    def printLog(self, container):
        def func(container):
            # Get the logs since current utc time as an iterator
            curTime = datetime.utcnow()
            logs = container.logs(stream=True, since=curTime)

            # Get the name and port setting
            name = container.name
            with open("./RecordData/config_record.json", "r") as f:
                matchDict = json.load(f)
                fileName = matchDict[name]
            with open(fileName) as f:
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
def getSystemPath(userPath: str):
    return str(os.path.normpath(userPath))
