import torch
import torchvision
import os
from threading import Lock
from flask_sqlalchemy import SQLAlchemy
from database.model import *
from utils.model_utils import *

IMAGENET_OUTPUT_SIZE = 1000

MODEL_INPUT_SHAPE = {
    "resnet-18": 224,
    "resnet-34": 224,
    "resnet-50": 224,
    "resnet-101": 224,
    "resnet-152": 224,
    "mobilenet-v2": 224,
    "resnet-18-32x32": 32,
    "alexnet": 227,
}

# TODO(Chonghan): Change this class to RModelManager later.
class RModelWrapper:
    def __init__(
        self, db_conn, network_type, net_path, device, pretrained, num_classes
    ):
        # self.device = torch.device(device)
        self.db_conn: SQLAlchemy = db_conn
        if pretrained:
            assert (
                num_classes == IMAGENET_OUTPUT_SIZE
            ), f"Pretrained model is supposed to have {IMAGENET_OUTPUT_SIZE} classes as output. "
        self.device = device  # We keep device as string to allow for easy comparison
        self.model = None
        self.model_meta_data = None
        self.model_name = ""
        self.init_model(network_type, pretrained, num_classes)
        self.num_classes = num_classes
        self.modelwork_type = network_type
        self._lock = Lock()
        self._model_available = True

        if os.path.exists(net_path):
            print("Loading previous checkpoint at {}".format(net_path))
            self.load_net(net_path)
        else:
            print("Checkpoint file not found: {}".format(net_path))

    def set_current_model(self, model_name: str):
        # No change if this model is already the current model
        if model_name == self.model_name:
            return

        # Free up current model.
        # TODO: make sure this model is GC'ed
        if self.model is not None:
            del self.model
            self.model = None

        self.model_name, self.model_meta_data = load_model_by_name(model_name)

    def init_model(self, network_type, pretrained, num_classes):
        if network_type == "resnet-18":
            self.model = torchvision.models.resnet18(
                pretrained=pretrained, num_classes=num_classes
            ).to(self.device)
        elif network_type == "resnet-34":
            self.model = torchvision.models.resnet34(
                pretrained=pretrained, num_classes=num_classes
            ).to(self.device)
        elif network_type == "resnet-50":
            self.model = torchvision.models.resnet50(
                pretrained=pretrained, num_classes=num_classes
            ).to(self.device)
        elif network_type == "resnet-101":
            self.model = torchvision.models.resnet101(
                pretrained=pretrained, num_classes=num_classes
            ).to(self.device)
        elif network_type == "resnet-152":
            self.model = torchvision.models.resnet152(
                pretrained=pretrained, num_classes=num_classes
            ).to(self.device)
        elif network_type == "mobilenet-v2":
            self.model = torchvision.models.mobilenet_v2(
                pretrained=pretrained, num_classes=num_classes
            ).to(self.device)
        elif network_type == "resnet-18-32x32":
            self.model = torchvision.models.ResNet(
                torchvision.models.resnet.BasicBlock,
                [2, 2, 2, 2],
                num_classes=num_classes,
            )
            self.model.conv1 = torch.nn.Conv2d(
                3, 64, kernel_size=3, stride=1, padding=1, bias=False
            )
            self.model.maxpool = torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
            self.model = self.model.to(self.device)
        elif network_type == "alexnet":
            self.model = torchvision.models.alexnet(
                pretrained=pretrained, num_classes=num_classes
            ).to(self.device)
        else:
            raise NotImplementedError(
                "Requested model type not supported. Please check."
            )

    def load_net(self, path):
        if os.path.exists(path):
            print("load net from: ", path)
            self.model.load_state_dict(torch.load(path, map_location=self.device))
        else:
            print("weight file not found")

    def acquire_model(self):
        """
        A thread-safe way to acquire access to the model. This is to make sure that only one
        thread can own the model at a time to avoid conflicts in gradient calculation. Always call
        this function before using the model (e.g., training, inferencing, ...)

        Return True if the model is available, False otherwise.
        """
        self._lock.acquire()

        if self._model_available:
            self._model_available = False
            self._lock.release()
            return True

        self._lock.release()
        return False

    def release_model(self):
        """
        Release the model so that other threads can use it
        """
        self._lock.acquire()
        self._model_available = True
        self._lock.release()

    def create_model(self, fields: dict):
        # TODO: Need to validate fields, dump model definition to a file,
        # etc. Either do these here or somewhere else

        model = Models(**fields)
        self.db_conn.session.add(model)
        self.db_conn.session.commit()

    def list_models(self) -> Models:
        return Models.query.all()

    def delete_model_by_name(self, name):
        model_to_delete = Models.query.filter_by(name=name).first()
        if model_to_delete:
            db.session.delete(model_to_delete)
            db.session.commit()
            return model_to_delete
        else:
            print(
                f"Attempting to delete a model that does not exist. Model name: {name}"
            )
            return None

    def get_current_model(self):
        return self.model

    def get_current_model_metadata(self):
        return self.model_meta_data

    def get_model_by_name(self, name):
        return Models.query.filter_by(name=name).first()
