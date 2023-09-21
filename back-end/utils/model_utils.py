import os
import importlib
import torch
import torchvision
from objects.RServer import RServer
from utils.predict import get_image_prediction
from database.model import *


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


# TODO: Use real model wrapper instead of dummy model wrapper
class DummyModelWrapper:
    def __init__(self, model):
        self.model = model
        self.device = RServer.get_model_wrapper().device


def init_predefined_model(name, pretrained, num_classes):
    """Initialize the predefined model with the specified name"""
    # Check if the model name is valid
    if name not in PREDEFINED_MODELS:
        raise Exception(f"Predefined model name {name} not recognized.")

    # If the model is pretrained, it should have the same number of classes as the ImageNet model
    if pretrained and num_classes != IMAGENET_OUTPUT_SIZE:
        raise Exception(
            f"Pretrained model is supposed to have {IMAGENET_OUTPUT_SIZE} classes as output."
        )

    if name == "ResNet18":
        model = torchvision.models.resnet18(
            pretrained=pretrained, num_classes=num_classes
        )
    elif name == "ResNet34":
        model = torchvision.models.resnet34(
            pretrained=pretrained, num_classes=num_classes
        )
    elif name == "ResNet50":
        model = torchvision.models.resnet50(
            pretrained=pretrained, num_classes=num_classes
        )
    elif name == "ResNet101":
        model = torchvision.models.resnet101(
            pretrained=pretrained, num_classes=num_classes
        )
    elif name == "ResNet152":
        model = torchvision.models.resnet152(
            pretrained=pretrained, num_classes=num_classes
        )
    elif name == "mobilenet-v2":
        model = torchvision.models.mobilenet_v2(
            pretrained=pretrained, num_classes=num_classes
        )
    elif name == "ResNet18-32x32":
        model = torchvision.models.ResNet(
            torchvision.models.resnet.BasicBlock, [2, 2, 2, 2], num_classes=num_classes
        )
        model.conv1 = torch.nn.Conv2d(
            3, 64, kernel_size=3, stride=1, padding=1, bias=False
        )
        model.maxpool = torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        if pretrained:
            raise Exception("Pretrained ResNet18-32x32 is not available.")
    elif name == "AlexNet":
        model = torchvision.models.alexnet(
            pretrained=pretrained, num_classes=num_classes
        )

    return model


def init_custom_model(code_path, name):
    """Initialize the custom model by importing the class with the specified name in the file specified by code_path"""
    try:
        spec = importlib.util.spec_from_file_location("model_def", code_path)
        model_def = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model_def)
        model = getattr(model_def, name)()
        return model
    except Exception as e:
        print("Failed to initialize the model.")
        print(e)
        raise e


def clear_model_temp_files(saving_id):
    """Clear the temporary files associated with the model"""
    code_path = os.path.join(
        RServer.get_server().base_dir, "generated", "models", f"{saving_id}.py"
    )
    weight_path = os.path.join(
        RServer.get_server().base_dir, "generated", "models", f"{saving_id}.pth"
    )
    try:
        if os.path.exists(code_path):
            os.remove(code_path)
        if os.path.exists(weight_path):
            os.remove(weight_path)
    except Exception as e:
        print("Failed to clear the temporary files associated with the model.")
        print(e)
        raise e


def val_model(model):
    """Validate the model by running the model against a small portion of the validation dataset"""
    # Get at most 10 samples from the validation dataset
    data_manager = RServer.get_data_manager()
    dataset = data_manager.validationset
    samples = dataset.samples[:10]
    # Create a dummy model wrapper to pass to the predict function
    dummy_model_wrapper = DummyModelWrapper(model)
    dummy_model_wrapper.model.eval()

    # Run the model against the samples
    for img_path, label in samples:
        get_image_prediction(
            dummy_model_wrapper,
            img_path,
            data_manager.image_size,
            argmax=False,
        )


def list_models():
    return RServer.get_model_wrapper().list_models()


def delete_model_by_name(model_name: str):
    return RServer.get_model_wrapper().delete_model_by_name(model_name)


def get_model_by_name(model_name: str) -> Models:
    return RServer.get_model_wrapper().get_model_by_name(model_name)


def get_current_model_metadata() -> Models:
    return RServer.get_model_wrapper().get_current_model_metadata()


def load_model_by_name(model_name: str):
    model_meta_data = get_model_by_name(model_name)
    model = init_custom_model(model_meta_data.code_path, model_name)
    model.load_state_dict(torch.load(model_meta_data.weight_path))
    return model, model_meta_data
