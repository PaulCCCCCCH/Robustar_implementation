import os
import time
import json

from test_app import app, client


class TestModel:
    class TestSetCurrentModel:
        def test_set_current_model(self, client):
            model0 = "model-non-exist"
            response = client.post(f"/model/current/{model0}")
            assert response.status_code != 200

    class TestUploadModel:
        def test_upload_model(self, client):

            metadata = {
                "class_name": "ResNet18",
                "nickname": "test_model",
                "description": "test description",
                "tags": ["tag1", "tag2"],
                "pretrained": "1",
                "num_classes": "1000",
            }

            response = client.post(
                f"/model", data=metadata, content_type="multipart/form-data"
            )

            assert response.status_code == 200
