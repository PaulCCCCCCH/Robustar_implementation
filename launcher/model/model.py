from PySide2.QtCore import QObject, Signal

class Model(QObject):
    # Custom signals
    containerNameChanged = Signal(str)
    imageVersionChanged = Signal(str)
    websitePortChanged = Signal(str)
    backendPortChanged = Signal(str)
    tensorboardPortChanged = Signal(str)
    trainPathChanged = Signal(str)
    testPathChanged = Signal(str)
    checkPointPathChanged = Signal(str)
    influencePathChanged = Signal(str)
    configFileChanged = Signal(str)



    def __init__(self, ctrl):
        super().__init__()

        self.ctrl = ctrl

        # Profile of the createTab
        self._profile = {
            'containerName': 'robustar',
            'imageVersion': 'cuda11.1-0.1.0-beta',
            'websitePort': '8000',
            'backendPort': '6848',
            'tensorboardPort': '6006',
            'trainPath': '',
            'testPath': '',
            'checkPointPath': '',
            'influencePath': '',
            'configFile': ''
        }

        # Root path of the path choosing window
        self.cwd = '/'

        # Selected container
        self.container = None

        # Name of the container to be operated on
        self.tempName = ''

        # Image version of the container to be operated on
        self.tempVer = ''

        # Website port of the container to be operated on
        self.tempWPort = ''

        # Boolean to record if the instruction is made on createTab
        self.madeOnCreateTab = False



        # Match the corresponding signals to slots in controllers
        self.containerNameChanged.connect(self.ctrl.setVContainerName)
        self.imageVersionChanged.connect(self.ctrl.setVImageVersion)
        self.websitePortChanged.connect(self.ctrl.setVWebsitePort)
        self.backendPortChanged.connect(self.ctrl.setVBackendPort)
        self.tensorboardPortChanged.connect(self.ctrl.setVTensorboardPort)
        self.trainPathChanged.connect(self.ctrl.setVTrainPath)
        self.testPathChanged.connect(self.ctrl.setVTestPath)
        self.checkPointPathChanged.connect(self.ctrl.setVCheckPointPath)
        self.influencePathChanged.connect(self.ctrl.setVInfluencePath)
        self.configFileChanged.connect(self.ctrl.setVConfigFile)





    @property
    def containerName(self):
        return self._profile['containerName']

    @containerName.setter
    def containerName(self, val):
        self._profile['containerName'] = val
        self.containerNameChanged.emit(val)

    @property
    def imageVersion(self):
        return self._profile['imageVersion']

    @imageVersion.setter
    def imageVersion(self, val):
        self._profile['imageVersion'] = val
        self.imageVersionChanged.emit(val)

    @property
    def websitePort(self):
        return self._profile['websitePort']

    @websitePort.setter
    def websitePort(self, val):
        self._profile['websitePort'] = val
        self.websitePortChanged.emit(val)

    @property
    def backendPort(self):
        return self._profile['backendPort']

    @backendPort.setter
    def backendPort(self, val):
        self._profile['backendPort'] = val
        self.backendPortChanged.emit(val)

    @property
    def tensorboardPort(self):
        return self._profile['tensorboardPort']

    @tensorboardPort.setter
    def tensorboardPort(self, val):
        self._profile['tensorboardPort'] = val
        self.tensorboardPortChanged.emit(val)

    @property
    def trainPath(self):
        return self._profile['trainPath']

    @trainPath.setter
    def trainPath(self, val):
        self._profile['trainPath'] = val
        self.trainPathChanged.emit(val)

    @property
    def testPath(self):
        return self._profile['testPath']

    @testPath.setter
    def testPath(self, val):
        self._profile['testPath'] = val
        self.testPathChanged.emit(val)

    @property
    def checkPointPath(self):
        return self._profile['checkPointPath']

    @checkPointPath.setter
    def checkPointPath(self, val):
        self._profile['checkPointPath'] = val
        self.checkPointPathChanged.emit(val)

    @property
    def influencePath(self):
        return self._profile['influencePath']

    @influencePath.setter
    def influencePath(self, val):
        self._profile['influencePath'] = val
        self.influencePathChanged.emit(val)

    @property
    def configFile(self):
        return self._profile['configFilePath']

    @configFile.setter
    def configFile(self, val):
        self._profile['configFile'] = val
        self.configFileChanged.emit(val)

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, val):
        self.containerName = val['containerName']
        self.imageVersion = val['imageVersion']
        self.websitePort = val['websitePort']
        self.backendPort = val['backendPort']
        self.tensorboardPort = val['tensorboardPort']
        self.trainPath = val['trainPath']
        self.testPath = val['testPath']
        self.checkPointPath = val['checkPointPath']
        self.influencePath = val['influencePath']
        self.configFile = val['configFile']
