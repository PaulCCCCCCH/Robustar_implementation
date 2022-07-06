import docker
import json
import os

from PySide2.QtCore import QObject

from controllers.main_ctrl import MainController

class DockerController(QObject):
    def __init__(self, model, view):
        super().__init__()

        self.model = model
        self.mainView = view

        # Initialize the client to communicate with the Docker daemon
        self.client = docker.from_env()

    def getSelection(self, forStart=False):
        if (self.mainView.ui.tabWidget.currentIndex() == 0):
            self.model.madeOnCreateTab = True
            self.model.tempName = self.model.profile['containerName']
            if(forStart == True):
                self.model.tempVer = self.model.profile['imageVersion']
                self.model.tempWPort = self.model.profile['websitePort']
            return self.getContainerByName(self.model.tempName, forStart=forStart)
        else:
            self.model.madeOnCreateTab = False
            items = MainController.getItemsFromListWidgets()
            if (len(items) == 0):
                self.model.tempName = None
                self.model.container = None
                MainController.printMessage(self.mainView.ui.promptBrowser, 'Please select a container first')
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
                MainController.printMessage(self.mainView.ui.promptBrowser, 'Can not find {}. Refresh <i>Manage</i> page to check the latest information'.format(self.model.tempName))
                return 1
        except docker.errors.APIError as apiError:
            MainController.printMessage(self.mainView.ui.promptBrowser,
                                        'Unexpected error encountered. See more in <i>Details</i> page')
            MainController.printMessage(self.mainView.ui.detailBrowser, str(apiError))
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

        configFile = self.model.profile['configFile']
        f = open(configFile)
        config = json.load(f)
        device = config['device']

        try:
            if 'cuda' in image and 'cuda' in device:
                self.startNewCudaServer()
            elif 'cpu' in image and 'cpu' in device:
                self.startNewCpuServer()
            else:
                MainController.printMessage(self.mainView.ui.promptBrowser,
                                                           "The image version doesn't match the device. Fail to create the container")
                return

            MainController.printMessage(self.mainView.ui.promptBrowser, 'Running {}'.format(self.model.tempVer))
            MainController.printMessage(self.mainView.ui.promptBrowser, '{} is available at http://localhost:{}'.format(self.model.tempName, self.model.tempWPort))
            MainController.addItem(self.mainView.ui.runningListWidget, self.model.tempName)

            # self.printLogs(self.model.container)


        except docker.errors.APIError as apiError:

            if ('port is already allocated' in str(apiError)):

                MainController.addItem(self.mainView.ui.createdListWidget, self.model.tempName)
                MainController.printMessage(self.mainView.ui.promptBrowser, '{} is created but fails to run because port is already allocated. See more in <i>Details</i> page'.format(self.model.tempName))
                MainController.printMessage(self.mainView.ui.detailBrowser, str(apiError))

            else:
                MainController.printMessage(self.mainView.ui.promptBrowser,
                                            'Unexpected error encountered. See more in <i>Details</i> page')
                MainController.printMessage(self.mainView.ui.detailBrowser, str(apiError))






    def startNewCpuServer(self, image):
        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile['containerName'],
            ports={
                '80/tcp': (
                    '127.0.0.1', int(self.model.profile['websitePort'])),
                '8000/tcp': ('127.0.0.1', 6848),
                '6006/tcp': ('127.0.0.1', 6006),
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
                getSystemPath(self.model.profile['configFile']) + ':/Robustar2/configs.json']
        )

    def startNewCudaServer(self, image):
        self.model.container = self.client.containers.run(
            image,
            detach=True,
            name=self.model.profile['containerName'],
            ports={
                '80/tcp': (
                    '127.0.0.1', int(self.model.profile['websitePort'])),
                '8000/tcp': ('127.0.0.1', 6848),
                '6006/tcp': ('127.0.0.1', 6006),
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
                self.model.profile['configFile'] + ':/Robustar2/configs.json'],

            # Set the device_requests parm
            device_requests=[
                docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])
            ]
        )

    def startExistServer(self):
        if self.model.container.status == 'exited':
            self.model.container.restart()
            self.customSignals.printMessageSignal.emit(self.mainView.ui.promptBrowser,
                                                       self.model.container.name + ' is available at http://localhost:' +
                                                       self.profile['websitePort'])
            self.customSignals.addItemSignal.emit(self.mainView.ui.runningListWidget, self.model.container.name)
            self.customSignals.removeItemSignal.emit(self.mainView.ui.exitedListWidget, self.model.container.name)

            # self.printLogs(self.model.container)



        elif self.model.container.status == 'created':
            self.model.container.start()
            self.customSignals.printMessageSignal.emit(self.mainView.ui.promptBrowser,
                                                       self.model.container.name + ' is available at http://localhost:' +
                                                       self.profile['websitePort'])
            self.customSignals.addItemSignal.emit(self.mainView.ui.runningListWidget, self.model.container.name)
            self.customSignals.removeItemSignal.emit(self.mainView.ui.createdListWidget, self.model.container.name)

            self.printLogs(self.model.container)

        # If the container is running
        elif self.model.container.status == 'running':
            self.customSignals.printMessageSignal.emit(self.mainView.ui.promptBrowser, self.model.container.name + ' is running')

        # If the container is in other status
        else:
            self.customSignals.printMessageSignal.emit(self.mainView.ui.promptBrowser, 'Illegal container status encountered')


# Change path input by the user to system path
def getSystemPath(userPath: str):
    return str(os.path.normpath(userPath))
