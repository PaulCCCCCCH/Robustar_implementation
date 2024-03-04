from PySide2.QtCore import QObject, Signal


class Model(QObject):
    # Custom signals
    nameChanged = Signal(str)
    imageChanged = Signal(str)
    portChanged = Signal(str)
    deviceChanged = Signal(str)
    clsChanged = Signal(str)
    sizeChanged = Signal(str)
    padChanged = Signal(str)
    trainPathChanged = Signal(str)
    valPathChanged = Signal(str)
    testPathChanged = Signal(str)
    pairedPathChanged = Signal(str)
    infPathChanged = Signal(str)
    outPathChanged = Signal(str)

    def __init__(self, ctrl):
        super().__init__()

        self.ctrl = ctrl

        # Profile of the createTab
        self._profile = {
            "name": "robustar",
            "image": "",
            "port": "8000",
            "device": "cpu",
            "cls": "",
            "size": "",
            "pad": "short_side",
            "train_path": "",
            "val_path": "",
            "test_path": "",
            "paired_path": "",
            "inf_path": "",
            "out_path": "",
        }

        # Root path of the path choosing window
        self.cwd = "/"

        # Selected container
        self.container = None

        # Name of the container to be operated on
        self.temp_name = ""

        # Image version of the container to be operated on
        self.temp_image = ""

        # Website port of the container to be operated on
        self.temp_port = ""

        # Boolean to record if the instruction is made on createTab
        self.made_on_create = False

        # Match the corresponding signals to slots in controllers
        self.nameChanged.connect(self.ctrl.set_v_name)
        self.imageChanged.connect(self.ctrl.set_v_image)
        self.portChanged.connect(self.ctrl.set_v_port)
        self.deviceChanged.connect(self.ctrl.set_v_device)
        self.clsChanged.connect(self.ctrl.set_v_cls)
        self.sizeChanged.connect(self.ctrl.set_v_size)
        self.padChanged.connect(self.ctrl.set_v_pad)
        self.trainPathChanged.connect(self.ctrl.set_v_train_path)
        self.valPathChanged.connect(self.ctrl.set_v_val_path)
        self.testPathChanged.connect(self.ctrl.set_v_test_path)
        self.pairedPathChanged.connect(self.ctrl.set_v_paired_path)
        self.infPathChanged.connect(self.ctrl.set_v_inf_path)
        self.outPathChanged.connect(self.ctrl.set_v_out_path)

    @property
    def name(self):
        return self._profile["name"]

    @name.setter
    def name(self, val):
        self._profile["name"] = val
        self.nameChanged.emit(val)

    @property
    def image(self):
        return self._profile["image"]

    @image.setter
    def image(self, val):
        self._profile["image"] = val
        self.imageChanged.emit(val)

    @property
    def port(self):
        return self._profile["port"]

    @port.setter
    def port(self, val):
        self._profile["port"] = val
        self.portChanged.emit(val)

    @property
    def device(self):
        return self._profile["device"]

    @device.setter
    def device(self, val):
        self._profile["device"] = val
        self.deviceChanged.emit(val)

    @property
    def cls(self):
        return self._profile["cls"]

    @cls.setter
    def cls(self, val):
        self._profile["cls"] = val
        self.clsChanged.emit(val)

    @property
    def size(self):
        return self._profile["size"]

    @size.setter
    def size(self, val):
        self._profile["size"] = val
        self.sizeChanged.emit(val)

    @property
    def pad(self):
        return self._profile["pad"]

    @pad.setter
    def pad(self, val):
        self._profile["pad"] = val
        self.padChanged.emit(val)

    @property
    def train_path(self):
        return self._profile["train_path"]

    @train_path.setter
    def train_path(self, val):
        self._profile["train_path"] = val
        self.trainPathChanged.emit(val)

    @property
    def val_path(self):
        return self._profile["val_path"]

    @val_path.setter
    def val_path(self, val):
        self._profile["val_path"] = val
        self.valPathChanged.emit(val)

    @property
    def test_path(self):
        return self._profile["test_path"]

    @test_path.setter
    def test_path(self, val):
        self._profile["test_path"] = val
        self.testPathChanged.emit(val)

    @property
    def paired_path(self):
        return self._profile["paired_path"]

    @paired_path.setter
    def paired_path(self, val):
        self._profile["paired_path"] = val
        self.pairedPathChanged.emit(val)

    @property
    def inf_path(self):
        return self._profile["inf_path"]

    @inf_path.setter
    def inf_path(self, val):
        self._profile["inf_path"] = val
        self.infPathChanged.emit(val)

    @property
    def out_path(self):
        return self._profile["out_path"]

    @out_path.setter
    def out_path(self, val):
        self._profile["out_path"] = val
        self.outPathChanged.emit(val)

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, val):
        self.name = val["name"]
        self.image = val["image"]
        self.port = val["port"]
        self.device = val["device"]
        self.cls = val["cls"]
        self.size = val["size"]
        self.pad = val["pad"]
        self.train_path = val["train_path"]
        self.val_path = val["val_path"]
        self.test_path = val["test_path"]
        self.paired_path = val["paired_path"]
        self.inf_path = val["inf_path"]
        self.out_path = val["out_path"]
