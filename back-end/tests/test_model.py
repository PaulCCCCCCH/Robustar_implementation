import os
import pytest
from .utils import dummy_api_list_models, dummy_api_delete_model, dummy_api_upload_dummy_model, dummy_api_set_current_model, dummy_api_get_current_model, must_succeed
from werkzeug.datastructures import FileStorage


code = """import torch
import torch.nn as nn


class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)

        # Activation and pooling
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)

        # Fully connected layers
        self.fc1 = nn.Linear(32 * 8 * 8, 128)  # after two pooling operations, 32x32 becomes 8x8
        self.fc2 = nn.Linear(128, 9)  # for 9 output classes

    def forward(self, x):
        # First convolutional layer followed by activation and pooling
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)

        # Second convolutional layer followed by activation and pooling
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)

        # Flatten the tensor
        x = x.view(-1, 32 * 8 * 8)

        # First fully connected layer followed by activation
        x = self.fc1(x)
        x = self.relu(x)

        # Second fully connected layer to produce the final output
        x = self.fc2(x)

        return x


if __name__ == "__main__":
    model = SimpleCNN()

    # Save the model checkpoint
    torch.save(model.state_dict(), "./SimpleCNN.pth")"""

wrong_code = code
wrong_code = wrong_code.replace(
    "self.fc2 = nn.Linear(128, 9)", "self.fc2 = nn.Linear(128, 10)"
)


# Test cases for upload_model
upload_test_cases = [
    {
        "input": {
            "metadata": """{
                "class_name": "SimpleCNN",
                "nickname": "custom-with-weight",
                "predefined": "0",
                "pretrained": "0",
                "description": "Simple CNN classifier.",
                "tags": ["test", "CNN"]
            }""",
            "code": code,
            "weight_file": "SimpleCNN.pth",
        },
        "expected_output": 200,
    },
    {
        "input": {
            "metadata": """{
                "class_name": "WrongName",
                "nickname": "custom-wrong-class-name",
                "predefined": "0",
                "pretrained": "0",
                "description": "Simple CNN classifier.",
                "tags": ["test", "CNN"]
            }""",
            "code": code,
            "weight_file": "SimpleCNN.pth",
        },
        "expected_output": 400,
    },
    {
        "input": {
            "metadata": """{
                "class_name": "SimpleCNN",
                "nickname": "custom-without-weight",
                "predefined": "0",
                "pretrained": "0",
                "description": "Simple CNN classifier.",
                "tags": ["test", "CNN"]
            }""",
            "code": code,
        },
        "expected_output": 200,
    },
    {
        "input": {
            "metadata": """{
                "class_name": "SimpleCNN",
                "nickname": "custom-without-code",
                "predefined": "0",
                "pretrained": "0",
                "description": "Simple CNN classifier.",
                "tags": ["test", "CNN"]
            }""",
            "weight_file": "SimpleCNN.pth",
        },
        "expected_output": 400,
    },
    {
        "input": {
            "metadata": """{
            "class_name": "SimpleCNN",
            "nickname": "custom-with-wrong-code",
            "predefined": "0",
            "pretrained": "0",
            "description": "Simple CNN classifier.",
            "tags": ["test", "CNN"]
        }""",
            "code": wrong_code,
        },
        "expected_output": 400,
    },
    {
        "input": {
            "metadata": """{
                "class_name": "SimpleCNN",
                "nickname": "without-description-tags",
                "predefined": "0",
                "pretrained": "0"
            }""",
            "code": code,
            "weight_file": "SimpleCNN.pth",
        },
        "expected_output": 200,
    },
    {
        "input": {
            "metadata": """{
                "class_name": "resnet-34",
                "nickname": "predefined-nonpretrained",
                "predefined": "1",
                "pretrained": "0",
                "description": "Predefined ResNet 34 without pretrained weights.",
                "tags": ["test", "CNN", "resnet"]
            }""",
        },
        "expected_output": 200,
    },
    {
        "input": {
            "metadata": """{
                "class_name": "resnet-34",
                "nickname": "predefined-pretrained",
                "predefined": "1",
                "pretrained": "1",
                "description": "Predefined ResNet 34 which is pretrained.",
                "tags": ["test", "CNN", "resnet"]
            }""",
        },
        "expected_output": 200,
    },
    {
        "input": {
            "metadata": """{
                "class_name": "resnet-34",
                "nickname": "predefined-pretrained",
                "predefined": "1",
                "pretrained": "1",
                "description": "Predefined ResNet 34 specified to be pretrained but with a weight file.",
                "tags": ["test", "CNN", "resnet"]
            }""",
            "weight_file": "SimpleCNN.pth",
        },
        "expected_output": 400,
    },
    {
        "input": {
            "metadata": """{
                "class_name": "undefined-name",
                "nickname": "undefined-name",
                "predefined": "1",
                "pretrained": "1",
                "description": "Undefined model name for predefined model.",
                "tags": ["test", "CNN", "resnet"]
            }""",
        },
        "expected_output": 400,
    },
    {
        "input": {
            "metadata": """{
                "class_name": 1,
                "nickname": 1,
                "predefined": 1,
                "pretrained": "2",
                "description": 1,
                "tags": "test"
            }""",
            "code": code,
        },
        "expected_output": 400,
    },
]




"""
    Test Cases
"""
class TestModel:
    class TestModelUpload:
        @pytest.mark.parametrize("test_data", upload_test_cases)
        def test_model_upload(self, client, reset_db, basedir, test_data):
            input_data = test_data["input"].copy()

            if "weight_file" in input_data:
                weight_file_path = os.path.join(basedir, input_data["weight_file"])
                f = open(weight_file_path, "rb")
                input_data["weight_file"] = (
                    FileStorage(stream=f, filename="SimpleCNN.pth"),
                )

            response = client.post(
                "/model", data=input_data, content_type="multipart/form-data"
            )
            if "weight_file" in input_data:
                f.close()
            assert response.status_code == test_data["expected_output"]

    class TestModelSwitch:
        def test_set_nonexist(self, client, reset_db):
            model_id = 1
            response = client.post(f"/model/current/{model_id}")
            assert response.status_code != 200

        def test_get_set(self, client, reset_db):
            # Upload two models
            resp = dummy_api_upload_dummy_model(client)
            assert (
                resp.status_code == 200
            ), f"Fail to upload dummy model. {resp.get_json().get('detail')}"
            resp = dummy_api_upload_dummy_model(client)
            assert (
                resp.status_code == 200
            ), f"Fail to upload dummy model. {resp.get_json().get('detail')}"

            # Fail when no current model is set
            resp = dummy_api_get_current_model(client)
            assert resp.status_code == 400

            # Set current model to the first one
            resp = dummy_api_set_current_model(client, 1)
            assert (
                resp.status_code == 200
            ), f"Fail to set model-1 as current model. {resp.get_json().get('detail')}"

            resp = dummy_api_get_current_model(client)
            assert resp.status_code == 200
            assert (
                resp.get_json()["data"].get("id") == 1
            ), f"current model nickname does match expected value"

            # Set current model to the second one
            resp = dummy_api_set_current_model(client, 2)
            assert (
                resp.status_code == 200
            ), f"Fail to set model-2 as current model. {resp.get_json().get('detail')}"

            resp = dummy_api_get_current_model(client)
            assert resp.status_code == 200
            assert (
                resp.get_json()["data"].get("id") == 2
            ), f"current model nickname does match expected value"

    class TestCRUDModel:
        def test_list(self, client, reset_db):
            # Upload dummy models
            for _ in range(2):
                must_succeed(lambda: dummy_api_upload_dummy_model(client))

            # List models
            resp = dummy_api_list_models(client)
            assert resp.status_code == 200
            models = resp.get_json()["data"]
            assert len(models) == 2, "Unexpected number of models in the list"

            model_ids = [model["id"] for model in models]
            assert 1 in model_ids
            assert 2 in model_ids

        def test_delete(self, client, reset_db):
            # Upload dummy models
            for _ in range(2):
                must_succeed(lambda: dummy_api_upload_dummy_model(client))

            # Delete model
            resp = dummy_api_delete_model(client, 1)
            assert resp.status_code == 200
            assert (
                resp.get_json()["data"].get("id") == 1
            ), "Deleted model metadata is wrong"

            # Expect only 1 model left in the list
            resp = dummy_api_list_models(client)
            models = resp.get_json()["data"]
            assert len(models) == 1, "Unexpected number of models in the list"

        def test_delete_current(self, client, reset_db):
            # Upload dummy models
            must_succeed(lambda: dummy_api_upload_dummy_model(client))

            must_succeed(lambda: dummy_api_set_current_model(client, 1))

            # Deleting current model
            resp = dummy_api_delete_model(client, 1)
            assert resp.status_code == 200

            # No current model is selected
            resp = dummy_api_get_current_model(client)
            assert resp.status_code == 400
