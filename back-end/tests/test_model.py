import os
import time

import torch

from test_app import app, client


class TestModel:
    class TestSetCurrentModel:
        def test_start_test_thread_fail_invalid_split(self, client):
            data = {"split": "invalid"}
            model0 = "model-non-exist"
            response = client.post(f"/model/current/{model0}")
            assert response.status_code != 200

            model1 = "model-1"
            response = client.post(f"/model/current/{model1}")
            assert response.status_code == 200

            model2 = "model-2"
            response = client.post(f"/model/current/{model2}")
            assert response.status_code == 200
