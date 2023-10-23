import os
import time

import torch

from test_app import app, client


class TestModel:
    class TestSetCurrentModel:
        def test_set_current_model(self, client):
            model0 = "model-non-exist"
            response = client.post(f"/model/current/{model0}")
            assert response.status_code != 200
