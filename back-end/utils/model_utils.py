import os
import torch
import io
import contextlib
import json
import uuid
import traceback
from objects.RServer import RServer
from utils.predict import get_image_prediction
from datetime import datetime


# Used for model validation
class DummyModelWrapper:
    def __init__(self, model, device):
        self.model = model
        self.device = device


class ContextManager:
    def __init__(self):
        self.base_dir = RServer.get_server().base_dir

    def __enter__(self):
        self.create_models_dir()
        self.saving_id = str(uuid.uuid4())
        self.code_path = None
        self.weight_path = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            traceback.print_exc()
            self.clear_model_temp_files()
        self.saving_id = None
        self.code_path = None
        self.weight_path = None

    def init_code_path(self):
        self.code_path = os.path.join(
            self.base_dir,
            "generated",
            "models",
            "code",
            f"{self.saving_id}.py",
        )

    def init_weight_path(self):
        self.weight_path = os.path.join(
            self.base_dir,
            "generated",
            "models",
            "ckpt",
            f"{self.saving_id}.pth",
        )

    def create_models_dir(self):
        """Check if the folder for saving models exists, if not, create it"""
        models_dir = os.path.join(self.base_dir, "generated", "models")
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
        if not os.path.exists(os.path.join(models_dir, "code")):
            os.makedirs(os.path.join(models_dir, "code"))
        if not os.path.exists(os.path.join(models_dir, "ckpt")):
            os.makedirs(os.path.join(models_dir, "ckpt"))

    def clear_model_temp_files(self):
        """Clear the temporary files associated with the model"""
        if self.code_path:
            if os.path.exists(self.code_path):
                os.remove(self.code_path)
        if self.weight_path:
            if os.path.exists(self.weight_path):
                os.remove(self.weight_path)


def precheck_request_4_upload_model(request):
    errors = []

    # Check for the presence of metadata
    metadata_str = request.form.get("metadata")
    if not metadata_str:
        errors.append("The model metadata is missing.")
        return errors

    metadata = json.loads(metadata_str)

    # Check for the presence of data
    missing_keys = []
    required_keys = ["class_name", "nickname", "predefined", "pretrained"]
    for key in required_keys:
        if key not in metadata:
            missing_keys.append(key)
    if missing_keys:
        errors.append(
            f"The following metadata fields are missing: {', '.join(missing_keys)}"
        )

    if metadata.get("predefined") == "0":
        code = request.form.get("code")
        if not code:
            errors.append(
                "Model definition code is missing but required when predefined is '0'."
            )
    if metadata.get("pretrained") == "1":
        weight_file = request.files.get("weight_file")
        if weight_file:
            errors.append("Weight file should not be specified when pretrained is '1'.")

    # Additional checks for metadata fields
    if "class_name" in metadata and not isinstance(metadata["class_name"], str):
        errors.append("class_name should be a string")
    if "nickname" in metadata and not isinstance(metadata["nickname"], str):
        errors.append("nickname should be a string")
    if "predefined" in metadata:
        if metadata["predefined"] not in ["0", "1"]:
            errors.append("predefined should be a either '0' or '1'")
    if "description" in metadata and not isinstance(metadata["description"], str):
        errors.append("description should be a string")
    if "pretrained" in metadata:
        if metadata["pretrained"] not in ["0", "1"]:
            errors.append("pretrained should be a either '0' or '1'")
    if "tags" in metadata and not (
        isinstance(metadata["tags"], list)
        and all(isinstance(tag, str) for tag in metadata["tags"])
    ):
        errors.append("tags should be a list of strings")

    if len(errors) > 0:
        raise ValueError("; ".join(errors))


def val_model(model_wrapper: DummyModelWrapper):
    """Validate the model by running the model against a small portion of the validation dataset"""
    # Get at most 10 samples from the validation dataset
    data_manager = RServer.get_data_manager()
    dataset = data_manager.validationset
    samples = dataset.samples[:10]
    # Create a dummy model wrapper to pass to the predict function
    model_wrapper.model.eval()

    # Run the model against the samples
    for img_path, label in samples:
        pred = get_image_prediction(
            model_wrapper,
            img_path,
            data_manager.image_size,
            argmax=False,
        )

        # Check if the prediction has the correct shape
        if pred.shape != (1, RServer.get_model_wrapper().num_classes):
            raise ValueError(
                "The model's output shape is inconsistent with the number of classes."
            )


def save_code(code, code_path):
    with open(code_path, "w") as code_file:
        code_file.write(code)


def save_ckpt_weight(weight_file, weight_path):
    weight_file.save(weight_path)


def load_ckpt_weight(model, weight_path):
    model.load_state_dict(
        torch.load(
            weight_path, map_location=torch.device(RServer.get_model_wrapper().device)
        )
    )


def save_cur_weight(model, weight_path):
    torch.save(model.state_dict(), weight_path)


def construct_metadata_4_save(metadata, code_path, weight_path, model):
    # Construct the metadata for saving
    metadata_4_save = {
        "class_name": metadata.get("class_name"),
        "nickname": metadata.get("nickname"),
        "predefined": bool(int(metadata.get("predefined"))),
        "pretrained": bool(int(metadata.get("pretrained"))),
        "description": metadata.get("description"),
        "tags": metadata.get("tags", []),
        "create_time": datetime.now(),
        "code_path": code_path,
        "weight_path": weight_path,
    }

    # Save the model's architecture to the metadata
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        print(model)
    metadata_4_save["architecture"] = buffer.getvalue()

    return metadata_4_save
