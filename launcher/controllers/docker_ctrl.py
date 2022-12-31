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
        self.mainView = view
        self.mainCtrl = ctrl

        # Initialize the client to communicate with the Docker daemon
        self.client = docker.from_env()
        if platform == "linux" or platform == "linux2":
            self.apiClient = docker.APIClient(base_url='unix://var/run/docker.sock')
        elif platform == "win32":
            self.apiClient = docker.APIClient(base_url='tcp://localhost:2375')

    def getSelection(self, forStart=False):
        if (self.mainView.ui.tabWidget.currentIndex() == 0):
            self.model.madeOnCreateTab = True
            self.model.tempName = self.model.profile['containerName']
            if(forStart == True):
                self.model.tempVer = self.model.profile['imageVersion']
                self.model.tempPort = self.model.profile['port']
            return self.getContainerByName(self.model.tempName, forStart=forStart)
        else:
            self.model.madeOnCreateTab = False
            items = self.mainCtrl.getItemsFromListWidgets()
            if (len(items) == 0):
                self.model.tempName = None
                self.model.container = None
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, 'Please select a container first')
                return 1
            else:
                item = items[0]
                self.model.tempName = item.text()
                return self.getContainerByName(self.model.tempName, forStart=forStart)

    def getContainerByName(self, name, forStart):
        try:
            self.model.container = self.client.containers.get(name)
            return 0
        except docker.errors.NotFound:
            if(self.model.madeOnCreateTab and forStart == True):
                self.model.container = None
                return 0
            else:
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, 'Can not find {}. Refresh <i>Manage</i> page to check the latest information'.format(self.model.tempName))
                return 1
        except docker.errors.APIError as apiError:
            self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                        'Unexpected error encountered. See more in <i>Details</i> page')
            self.mainCtrl.printMessage(self.mainView.ui.detailBrowser, str(apiError))
            return 1

    def startServer(self):
        if(self.getSelection(forStart=True)):
            return
        if(self.model.container == None):
            self.startNewServer()
        else:
            self.startExistServer()


    def startNewServer(self):
        image = 'paulcccccch/robustar:' + self.model.profile['imageVersion']

        # save backend relevant configs in a json file
        config = {
            'model_arch': self.model.modelArch,
            'pre_trained': True if self.model.pretrained == 'True' else False,
            'weight_to_load': self.model.weightFile,
            'device': self.model.device,
            'shuffle': True if self.model.shuffle == 'True' else False,
            'batch_size': int(self.model.batchSize),
            'num_workers': int(self.model.workerNumber),
            'image_size': int(self.model.imgSize),
            'image_padding': self.model.padding,
            'num_classes': int(self.model.classNumber),
            'port': int(self.model.port)
        }

        # Create folder to store record data
        if not os.path.exists('./RecordData'):
            os.makedirs('./RecordData')

        fileName = f'./RecordData/config_{uuid.uuid4().hex}.json'
        with open(fileName, 'w') as f:
            f.write(json.dumps(config))
        configFile = os.path.join(os.getcwd(), fileName)

        # Store the (container - config file) matching
        if not os.path.exists('./RecordData/config_record.json'):
            matchDict = {}
        else:
            with open('./RecordData/config_record.json', 'r') as f:
                matchDict = json.load(f)
        with open('./RecordData/config_record.json', 'w') as f:
            matchDict[self.model.profile['containerName']] = fileName
            json.dump(matchDict, f)

        try:
            if 'cuda' in self.model.device:
                self.startNewCudaServer(image, configFile)
            elif 'cpu' in self.model.device:
                self.startNewCpuServer(image, configFile)

            self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, 'Running {}'.format(self.model.tempVer))
            self.mainCtrl.updateSucView()

            self.printLog(self.model.container)


        except docker.errors.APIError as apiError:

            if ('port is already allocated' in str(apiError)):

                self.mainCtrl.addItem(self.mainView.ui.createdListWidget, self.model.tempName)
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, '{} is created but fails to run because port is already allocated. See more in <i>Details</i> page'.format(self.model.tempName))
                self.mainCtrl.printMessage(self.mainView.ui.detailBrowser, str(apiError))

            else:
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                            'Unexpected error encountered. See more in <i>Details</i> page')
                self.mainCtrl.printMessage(self.mainView.ui.detailBrowser, str(apiError))
                with open('./RecordData/config_record.json', 'r') as f:
                    matchDict = json.load(f)
                with open('./RecordData/config_record.json', 'w') as f:
                    fileName = matchDict.pop(self.model.profile['containerName'])
                    os.remove(fileName)
                    json.dump(matchDict, f)


    def startNewCpuServer(self, image, configFile):
        self.downloadImage(image)

        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile['containerName'],
            ports={
                '80/tcp': (
                    '127.0.0.1', int(self.model.profile['port']))
            },
            mounts=[
                docker.types.Mount(target='/Robustar2/dataset/train',
                                   source=getSystemPath(self.model.profile['trainPath']),
                                   type='bind'),
                docker.types.Mount(target='/Robustar2/dataset/test',
                                   source=getSystemPath(self.model.profile['testPath']),
                                   type='bind'),
                docker.types.Mount(target='/Robustar2/influence_images',
                                   source=getSystemPath(self.model.profile['influencePath']),
                                   type='bind'),
                docker.types.Mount(
                    target='/Robustar2/checkpoints',
                    source=getSystemPath(self.model.profile['checkPointPath']),
                    type='bind'),
            ],
            volumes=[
                getSystemPath(configFile) + ':/Robustar2/configs.json']
        )

    def startNewCudaServer(self, image, configFile):
        self.downloadImage(image)

        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile['containerName'],
            ports={
                '80/tcp': (
                    '127.0.0.1', int(self.model.profile['port']))
            },
            mounts=[
                docker.types.Mount(target='/Robustar2/dataset/train',
                                   source=getSystemPath(self.model.profile['trainPath']),
                                   type='bind'),
                docker.types.Mount(target='/Robustar2/dataset/test',
                                   source=getSystemPath(self.model.profile['testPath']),
                                   type='bind'),
                docker.types.Mount(target='/Robustar2/influence_images',
                                   source=getSystemPath(self.model.profile['influencePath']),
                                   type='bind'),
                docker.types.Mount(
                    target='/Robustar2/checkpoints',
                    source=getSystemPath(self.model.profile['checkPointPath']),
                    type='bind'),
            ],
            volumes=[
                configFile + ':/Robustar2/configs.json'],

            # Set the device_requests parm
            device_requests=[
                docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])
            ]
        )

    def startExistServer(self):
        try:
            if self.model.container.status == 'exited':
                self.model.container.restart()
                self.mainCtrl.updateSucView()
                self.mainCtrl.removeItem(self.mainView.ui.exitedListWidget, self.model.tempName)

                self.printLog(self.model.container)

            elif self.model.container.status == 'created':
                self.model.container.start()
                self.mainCtrl.updateSucView()
                self.mainCtrl.removeItem(self.mainView.ui.createdListWidget, self.model.tempName)

                self.printLog(self.model.container)

            elif self.model.container.status == 'running':
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, '{} is running'.format(self.model.tempName))

            else:
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, 'Illegal container status encountered')
        except docker.errors.APIError as apiError:
            if ('port is already allocated' in str(apiError)):

                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, '{} fails to run because port is already allocated. See more in <i>Details</i> page'.format(self.model.tempName))
                self.mainCtrl.printMessage(self.mainView.ui.detailBrowser, str(apiError))

            else:
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                            'Unexpected error encountered. See more in <i>Details</i> page')
                self.mainCtrl.printMessage(self.mainView.ui.detailBrowser, str(apiError))

    def stopServer(self):
        if(self.getSelection()):
            return
        try:
            if self.model.container.status == 'exited':
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, '{} has already stopped'.format(self.model.tempName))

            elif self.model.container.status == 'created':
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, '{} is not running'.format(self.model.tempName))

            elif self.model.container.status == 'running':
                self.model.container.stop()
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, '{} is now stopped'.format(self.model.tempName))
                self.mainCtrl.addItem(self.mainView.ui.exitedListWidget, self.model.tempName)
                self.mainCtrl.removeItem(self.mainView.ui.runningListWidget, self.model.tempName)

            else:
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                                           'Illegal container status encountered')
        except docker.errors.APIError as apiError:
            self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                       'Unexpected error encountered. See more in <i>Details</i> page')
            self.mainCtrl.printMessage(self.mainView.ui.detailBrowser, str(apiError))

    def deleteServer(self):
        if(self.getSelection()):
            return
        try:
            if self.model.container.status == 'running' or self.model.container.status == 'created' or self.model.container.status == 'exited':
                self.model.container.remove()
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, '{} removed'.format(self.model.tempName))

                if(self.model.container.status == 'running'):
                    self.mainCtrl.removeItem(self.mainView.ui.runningListWidget, self.model.tempName)
                elif(self.model.container.status == 'created'):
                    self.mainCtrl.removeItem(self.mainView.ui.createdListWidget, self.model.tempName)
                elif (self.model.container.status == 'exited'):
                    self.mainCtrl.removeItem(self.mainView.ui.exitedListWidget, self.model.tempName)

                with open('./RecordData/config_record.json', 'r') as f:
                    matchDict = json.load(f)
                with open('./RecordData/config_record.json', 'w') as f:
                    fileName = matchDict.pop(self.model.tempName)
                    os.remove(fileName)
                    json.dump(matchDict, f)
            else:
                self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                                           'Illegal container status encountered')
        except docker.errors.APIError as apiError:
            self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                       'Unexpected error encountered. See more in <i>Details</i> page')
            self.mainCtrl.printMessage(self.mainView.ui.detailBrowser, str(apiError))

    def refreshServers(self):
        for listWidget in self.mainView.listWidgets:
            listWidget.clear()

        try:
            containerList = self.client.containers.list(all=True)

            for container in containerList:
                if ('paulcccccch/robustar:' in str(container.image)):
                    if (container.status == 'running'):
                        self.mainCtrl.addItem(self.mainView.ui.runningListWidget, container.name)

                        self.printLog(container)
                    elif (container.status == 'exited'):
                        self.mainCtrl.addItem(self.mainView.ui.exitedListWidget, container.name)
                    elif (container.status == 'created'):
                        self.mainCtrl.addItem(self.mainView.ui.createdListWidget, container.name)
                    else:
                        self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                                                   'Illegal container status encountered')
        except docker.errors.APIError as apiError:
            self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                       'Unexpected error encountered. See more in <i>Details</i> page')
            self.mainCtrl.printMessage(self.mainView.ui.detailBrowser, str(apiError))

    def downloadImage(self, image):
        imageList = [x.tags[0] for x in self.client.images.list() if x.tags != []]
        if image not in imageList:
            self.mainCtrl.printMessage(self.mainView.ui.promptBrowser,
                                       f'Downloading {image}. See more in <i>Details</i> page')
            repo, tag = image.split(':')
            for line in self.apiClient.pull(repository=repo, tag=tag, stream=True, decode=True):
                self.mainCtrl.printMessage(self.mainView.ui.detailBrowser, str(line))
            self.mainCtrl.printMessage(self.mainView.ui.promptBrowser, f'Downloaded {image}')

    def printLog(self, container):
        def func(container):
            # Get the logs since current utc time as an iterator
            curTime = datetime.utcnow()
            logs = container.logs(stream=True, since=curTime)

            # Get the name and port setting
            name = container.name
            with open('./RecordData/config_record.json', 'r') as f:
                matchDict = json.load(f)
                fileName = matchDict[name]
            with open(fileName) as f:
                config = json.load(f)
                port = config['port']

            # Print the logs until the container is stopped
            try:
                while True:
                    log = next(logs).decode("utf-8")

                    # Remove the color of log
                    log = re.sub('.\[\d+m', '', log)

                    # Add the name and port information
                    log = f'{name} - - ' + log[:log.find(' - -')] + f':{port}' + log[log.find(' - -'):]

                    self.mainCtrl.printMessage(self.mainView.ui.logBrowser, log, timestamp=False)
            except StopIteration:
                return

        t = Thread(target=func, args=(container,), daemon=True)
        t.start()


# Change path input by the user to system path
def getSystemPath(userPath: str):
    return str(os.path.normpath(userPath))
