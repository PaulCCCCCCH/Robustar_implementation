import torch
import torchvision
import os
from threading import Lock
from flask_sqlalchemy import SQLAlchemy
from database.model import Models, Tags, db
import importlib

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

AVAILABLE_MODELS = list(MODEL_INPUT_SHAPE.keys())

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

        # TODO: Should initialize to None. Remove in the future.
        self.model = RModelWrapper.init_pre_defined_model(
            network_type, pretrained, num_classes, self.device
        )
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

        # Get new model
        new_model_data, new_model_meta_data = self.load_model_by_name(model_name)
        if not new_model_data or not new_model_meta_data:
            raise ValueError("Model does not exist")

        # Free up current model.
        # TODO: make sure this model is GC'ed
        if self.model is not None:
            del self.model
            self.model = None

        self.model_name, self.model_meta_data = new_model_data, new_model_meta_data

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

        tags = fields.pop("tags", [])

        tag_objs = []
        if tags:
            for tag_name in tags:
                tag = self.db_conn.session.query(Tags).filter_by(name=tag_name).first()
                if tag is None:
                    tag = Tags(name=tag_name)
                    self.db_conn.session.add(tag)
                tag_objs.append(tag)

        model = Models(**fields, tags=tag_objs)
        self.db_conn.session.add(model)
        self.db_conn.session.commit()

    def list_models(self) -> list[Models]:
        return Models.query.all()

    def delete_model_by_name(self, name) -> Models:
        model_to_delete = Models.query.filter_by(nickname=name).first()
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

    @staticmethod
    def get_model_by_name(name) -> Models:
        return Models.query.filter_by(nickname=name).first()

    def load_model_by_name(self, model_name: str):
        model_meta_data = RModelWrapper.get_model_by_name(model_name)

        # TODO: need a way to distinguish between predefined and custom model
        if model_meta_data.class_name in AVAILABLE_MODELS:
            model = RModelWrapper.init_pre_defined_model(
                model_meta_data.class_name,
                False,
                self.num_classes,
                self.device,
            )
        else:
            model = RModelWrapper.init_custom_model(
                model_meta_data.code_path, model_name, self.device
            )
        model.load_state_dict(torch.load(model_meta_data.weight_path))
        return model, model_meta_data

    @staticmethod
    def init_pre_defined_model(network_type, pretrained, num_classes, device):
        if network_type == "resnet-18":
            model = torchvision.models.resnet18(
                pretrained=pretrained, num_classes=num_classes
            )
        elif network_type == "resnet-34":
            model = torchvision.models.resnet34(
                pretrained=pretrained, num_classes=num_classes
            )
        elif network_type == "resnet-50":
            model = torchvision.models.resnet50(
                pretrained=pretrained, num_classes=num_classes
            )
        elif network_type == "resnet-101":
            model = torchvision.models.resnet101(
                pretrained=pretrained, num_classes=num_classes
            )
        elif network_type == "resnet-152":
            model = torchvision.models.resnet152(
                pretrained=pretrained, num_classes=num_classes
            )
        elif network_type == "mobilenet-v2":
            model = torchvision.models.mobilenet_v2(
                pretrained=pretrained, num_classes=num_classes
            )
        elif network_type == "resnet-18-32x32":
            model = torchvision.models.ResNet(
                torchvision.models.resnet.BasicBlock,
                [2, 2, 2, 2],
                num_classes=num_classes,
            )
            model.conv1 = torch.nn.Conv2d(
                3, 64, kernel_size=3, stride=1, padding=1, bias=False
            )
            model.maxpool = torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        elif network_type == "alexnet":
            model = torchvision.models.alexnet(
                pretrained=pretrained, num_classes=num_classes
            )
        else:
            raise NotImplementedError(
                "Requested model type not supported. Please check."
            )

        return model.to(device)

    @staticmethod
    def init_custom_model(code_path, name, device):
        """Initialize the custom model by importing the class with the specified name in the file specified by code_path"""
        try:
            spec = importlib.util.spec_from_file_location("model_def", code_path)
            model_def = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(model_def)
            model = getattr(model_def, name)()
            return model.to(device)
        except Exception as e:
            print("Failed to initialize the model.")
            print(e)
            raise e
