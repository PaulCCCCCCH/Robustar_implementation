from PySide2.QtCore import QObject, Signal

class Model(QObject):
    # Custom signals
    containerNameChanged = Signal(str)
    imageVersionChanged = Signal(str)
    portChanged = Signal(str)
    trainPathChanged = Signal(str)
    testPathChanged = Signal(str)
    checkPointPathChanged = Signal(str)
    influencePathChanged = Signal(str)
    configFileChanged = Signal(str)
    modelArchChanged = Signal(str)
    pretrainedChanged = Signal(str)
    weightFileChanged = Signal(str)
    deviceChanged = Signal(str)
    shuffleChanged = Signal(str)
    batchSizeChanged = Signal(str)
    workerNumberChanged = Signal(str)
    imgSizeChanged = Signal(str)
    paddingChanged = Signal(str)
    classNumberChanged = Signal(str)

    def __init__(self, ctrl):
        super().__init__()

        self.ctrl = ctrl

        # Profile of the createTab
        self._profile = {
            'containerName': 'robustar',
            'imageVersion': '',
            'port': '8000',
            'trainPath': '',
            'testPath': '',
            'checkPointPath': '',
            'influencePath': '',
            'model_arch': 'resnet-18',
            'pre_trained': 'False',
            'weight_to_load': '',
            'device': 'cpu',
            'shuffle': 'False',
            'batch_size': '',
            'num_workers': '',
            'image_size': '',
            'padding': 'short side',
            'num_classes': ''
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
        self.tempPort = ''

        # Boolean to record if the instruction is made on createTab
        self.madeOnCreateTab = False


        # Match the corresponding signals to slots in controllers
        self.containerNameChanged.connect(self.ctrl.setVContainerName)
        self.imageVersionChanged.connect(self.ctrl.setVImageVersion)
        self.portChanged.connect(self.ctrl.setVPort)
        self.trainPathChanged.connect(self.ctrl.setVTrainPath)
        self.testPathChanged.connect(self.ctrl.setVTestPath)
        self.checkPointPathChanged.connect(self.ctrl.setVCheckPointPath)
        self.influencePathChanged.connect(self.ctrl.setVInfluencePath)
        self.modelArchChanged.connect(self.ctrl.setVModelArch)
        self.pretrainedChanged.connect(self.ctrl.setVPretrained)
        self.weightFileChanged.connect(self.ctrl.setVWeightFile)
        self.deviceChanged.connect(self.ctrl.setVDevice)
        self.shuffleChanged.connect(self.ctrl.setVShuffle)
        self.batchSizeChanged.connect(self.ctrl.setVBatchSize)
        self.workerNumberChanged.connect(self.ctrl.setVWorkerNumber)
        self.imgSizeChanged.connect(self.ctrl.setVImgSize)
        self.paddingChanged.connect(self.ctrl.setVPadding)
        self.classNumberChanged.connect(self.ctrl.setVClassNumber)

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
    def port(self):
        return self._profile['port']

    @port.setter
    def port(self, val):
        self._profile['port'] = val
        self.portChanged.emit(val)

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
    def modelArch(self):
        return self._profile['model_arch']

    @modelArch.setter
    def modelArch(self, val):
        self._profile['model_arch'] = val
        self.modelArchChanged.emit(val)

    @property
    def pretrained(self):
        return self._profile['pre_trained']

    @pretrained.setter
    def pretrained(self, val):
        self._profile['pre_trained'] = val
        self.pretrainedChanged.emit(val)

    @property
    def weightFile(self):
        return self._profile['weight_to_load']

    @weightFile.setter
    def weightFile(self, val):
        self._profile['weight_to_load'] = val
        self.weightFileChanged.emit(val)

    @property
    def device(self):
        return self._profile['device']

    @device.setter
    def device(self, val):
        self._profile['device'] = val
        self.deviceChanged.emit(val)

    @property
    def shuffle(self):
        return self._profile['shuffle']

    @shuffle.setter
    def shuffle(self, val):
        self._profile['shuffle'] = val
        self.shuffleChanged.emit(val)

    @property
    def batchSize(self):
        return self._profile['batch_size']

    @batchSize.setter
    def batchSize(self, val):
        self._profile['batch_size'] = val
        self.batchSizeChanged.emit(val)

    @property
    def workerNumber(self):
        return self._profile['num_workers']

    @workerNumber.setter
    def workerNumber(self, val):
        self._profile['num_workers'] = val
        self.workerNumberChanged.emit(val)

    @property
    def imgSize(self):
        return self._profile['image_size']

    @imgSize.setter
    def imgSize(self, val):
        self._profile['image_size'] = val
        self.imgSizeChanged.emit(val)

    @property
    def padding(self):
        return self._profile['padding']

    @padding.setter
    def padding(self, val):
        self._profile['padding'] = val
        self.paddingChanged.emit(val)

    @property
    def classNumber(self):
        return self._profile['num_classes']

    @classNumber.setter
    def classNumber(self, val):
        self._profile['num_classes'] = val
        self.classNumberChanged.emit(val)

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, val):
        self.containerName = val['containerName']
        self.imageVersion = val['imageVersion']
        self.port = val['port']
        self.trainPath = val['trainPath']
        self.testPath = val['testPath']
        self.checkPointPath = val['checkPointPath']
        self.influencePath = val['influencePath']
        self.modelArch = val['model_arch']
        self.pretrained = val['pre_trained']
        self.weightFile = val['weight_to_load']
        self.device = val['device']
        self.shuffle = val['shuffle']
        self.batchSize = val['batch_size']
        self.workerNumber = val['num_workers']
        self.imgSize = val['image_size']
        self.padding = val['padding']
        self.classNumber = val['num_classes']

