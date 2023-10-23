import os
import importlib
import torch
import torchvision
import io
import contextlib
from objects.RServer import RServer
from utils.predict import get_image_prediction
from datetime import datetime


IMAGENET_OUTPUT_SIZE = 1000

PREDEFINED_MODELS = [
    "ResNet18",
    "ResNet34",
    "ResNet50",
    "ResNet101",
    "ResNet152",
    "mobilenet-v2",
    "ResNet18-32x32",
    "AlexNet",
]


# TODO: Use the real model manager instead of dummy model manager
class DummyModelManager:
    def __init__(self, model):
        self.model = model
        self.device = RServer.get_model_manager().device


def init_predefined_model(class_name, pretrained, num_classes):
    """Initialize the predefined model with the specified name"""
    # Check if the model name is valid
    if class_name not in PREDEFINED_MODELS:
        raise Exception(f"Predefined model name {class_name} not recognized.")

    # If the model is pretrained, it should have the same number of classes as the ImageNet model
    if pretrained and num_classes != IMAGENET_OUTPUT_SIZE:
        raise Exception(
            f"Pretrained model is supposed to have {IMAGENET_OUTPUT_SIZE} classes as output."
        )

    if class_name == "ResNet18":
        model = torchvision.models.resnet18(
            pretrained=pretrained, num_classes=num_classes
        )
    elif class_name == "ResNet34":
        model = torchvision.models.resnet34(
            pretrained=pretrained, num_classes=num_classes
        )
    elif class_name == "ResNet50":
        model = torchvision.models.resnet50(
            pretrained=pretrained, num_classes=num_classes
        )
    elif class_name == "ResNet101":
        model = torchvision.models.resnet101(
            pretrained=pretrained, num_classes=num_classes
        )
    elif class_name == "ResNet152":
        model = torchvision.models.resnet152(
            pretrained=pretrained, num_classes=num_classes
        )
    elif class_name == "mobilenet-v2":
        model = torchvision.models.mobilenet_v2(
            pretrained=pretrained, num_classes=num_classes
        )
    elif class_name == "ResNet18-32x32":
        model = torchvision.models.ResNet(
            torchvision.models.resnet.BasicBlock, [2, 2, 2, 2], num_classes=num_classes
        )
        model.conv1 = torch.nn.Conv2d(
            3, 64, kernel_size=3, stride=1, padding=1, bias=False
        )
        model.maxpool = torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        if pretrained:
            raise Exception("Pretrained ResNet18-32x32 is not available.")
    elif class_name == "AlexNet":
        model = torchvision.models.alexnet(
            pretrained=pretrained, num_classes=num_classes
        )

    return model


def init_custom_model(code_path, class_name):
    """Initialize the custom model by importing the class with the specified name in the file specified by code_path"""
    spec = importlib.util.spec_from_file_location("model_def", code_path)
    model_def = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_def)
    model = getattr(model_def, class_name)()
    return model


def clear_model_temp_files(code_path, weight_path):
    """Clear the temporary files associated with the model"""
    if os.path.exists(code_path):
        os.remove(code_path)
    if os.path.exists(weight_path):
        os.remove(weight_path)


def val_model(model):
    """Validate the model by running the model against a small portion of the validation dataset"""
    # Get at most 10 samples from the validation dataset
    data_manager = RServer.get_data_manager()
    dataset = data_manager.validationset
    samples = dataset.samples[:10]
    # Create a dummy model wrapper to pass to the predict function
    dummy_model_manager = DummyModelManager(model)
    dummy_model_manager.model.eval()

    # Run the model against the samples
    for img_path, label in samples:
        get_image_prediction(
            dummy_model_manager,
            img_path,
            data_manager.image_size,
            argmax=False,
        )


def create_models_dir():
    # Check if the folder for saving models exists, if not, create it
    models_dir = os.path.join(RServer.get_server().base_dir, "generated", "models")
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(os.path.join(models_dir, "code")):
        os.makedirs(os.path.join(models_dir, "code"))
    if not os.path.exists(os.path.join(models_dir, "ckpt")):
        os.makedirs(os.path.join(models_dir, "ckpt"))


def save_code(code, code_path):
    with open(code_path, "w") as code_file:
        code_file.write(code)


def save_ckpt_weight(weight_file, weight_path):
    weight_file.save(weight_path)


def load_ckpt_weight(model, weight_path):
    model.load_state_dict(torch.load(weight_path))


def save_cur_weight(model, weight_path):
    torch.save(model.state_dict(), weight_path)


def construct_metadata_4_save(class_name, metadata, code_path, weight_path, model):
    # Construct the metadata for saving
    metadata_4_save = {
        "class_name": class_name,
        "nickname": metadata.get("nickname"),
        "description": metadata.get("description")
        if metadata.get("description")
        else None,
        "tags": metadata.get("tags") if metadata.get("tags") else None,
        "create_time": datetime.now(),
        "code_path": code_path,
        "weight_path": weight_path,
        "epoch": 0,
        "train_accuracy": None,
        "val_accuracy": None,
        "test_accuracy": None,
        "last_eval_on_dev_set": None,
        "last_eval_on_test_set": None,
    }

    # Save the model's architecture to the metadata
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        print(model)
    metadata_4_save["architecture"] = buffer.getvalue()

    return metadata_4_save
