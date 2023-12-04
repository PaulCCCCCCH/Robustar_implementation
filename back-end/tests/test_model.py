import os
import pytest
from werkzeug.datastructures import FileStorage
from test_app import app, client, basedir


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


# Test cases for upload_model
upload_test_cases = [
    {
        "input": {
            "metadata": """{
                "class_name": "custom-with-weight",
                "nickname": "simple-classifier",
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
                "class_name": "custom-without-weight",
                "nickname": "simple-classifier",
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
]


class TestModel:
    class TestSetCurrentModel:
        def test_set_current_model(self, client):
            model0 = "model-non-exist"
            response = client.post(f"/model/current/{model0}")
            assert response.status_code != 200

    class TestUploadModel:
        @pytest.mark.parametrize("test_data", upload_test_cases)
        def test_upload_model(self, client, basedir, test_data):
            input_data = test_data["input"].copy()

            if "weight_file_path" in input_data:
                weight_file_path = os.path.join(basedir, input_data["weight_file"])
                with open(weight_file_path, "rb") as f:
                    input_data["weight_file"] = (
                        FileStorage(stream=f, filename="SimpleCNN.pth"),
                    )

            response = client.post(
                "/model", data=input_data, content_type="multipart/form-data"
            )
            assert response.status_code == test_data["expected_output"]
