import os
import time
import json

from test_app import app, client


def get_dummy_model_metadata(nickname):
    metadata = {
        "class_name": "ResNet18",
        "nickname": nickname,
        "description": "test description",
        "tags": ["tag1", "tag2"],
        "pretrained": "0",
        "predefined": "1",
        "num_classes": "1000",
    }

    return metadata


def api_upload_dummy_model(client, name):
    metadata = get_dummy_model_metadata("test-resnet-18")

    response = client.post(f"/model", data=metadata, content_type="multipart/form-data")

    return response


def api_set_current_model(client, name):
    response = client.post(f"/model/current/{name}")
    return response


def api_get_current_model(client):
    response = client.get("/model/current")
    return response


class TestModel:
    class TestUploadModel:
        def test_upload_model(self, client):
            # TODO:
            response = api_upload_dummy_model(client, "test-resnet-18")
            assert response.status_code == 200

    class TestCurrentModel:
        def test_set_current_model_nonexist(self, client):
            model_name = "model-non-exist"
            response = client.post(f"/model/current/{model_name}")
            assert response.status_code != 200

        def test_get_current_model(self, client):
            api_upload_dummy_model(client, "model-1")
            api_upload_dummy_model(client, "model-2")

            # No model is selected
            resp = client.get(f"/model/current")
            assert resp.status_code == 400
