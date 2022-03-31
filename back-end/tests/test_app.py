import json
import os.path as osp

import pytest

from objects.RServer import RServer
from server import start_server


# baseDir = osp.join('/', 'Robustar2').replace('\\', '/')
# datasetDir = osp.join(baseDir, 'dataset').replace('\\', '/')
# ckptDir = osp.join(baseDir, 'checkpoints').replace('\\', '/')
# with open(osp.join(baseDir, 'configs.json')) as jsonfile:
#     configs = json.load(jsonfile)
#
# RServer.createServer(configs=configs, baseDir=baseDir, datasetDir=datasetDir, ckptDir=ckptDir)
#
# def test_valid_app_and_server():
#     server = RServer.getServer()
#     assert server
#     assert server.getFlaskApp()
#     # assert server.dataManager
#     # assert RServer.getModelWrapper()


@pytest.fixture()
def app():
    start_server()
    server = RServer.getServer()
    app = server.getFlaskApp()
    app.config['TESTING'] = True
    yield app
    app.config['TESTING'] = False


@pytest.fixture()
def client(app):
    return app.test_client()


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()


class TestConfig:

    def test_config(self, client):
        rv = client.get("/config").get_json()
        assert rv['code'] == 0
        assert rv['data'] == {
            "weight_to_load": "resnet-18.pth",
            "model_arch": "resnet-18-32x32",
            "device": "cpu",
            "pre_trained": False,
            "batch_size": 16,
            "shuffle": True,
            "num_workers": 8,
            "image_size": 32,
            "image_padding": "none",
            "num_classes": 9
        }

# class TestPredict:
#
#     def test_predict(self, client):
#         rv = client.get("/backend_test/train/1")
#         res = json.loads(rv.data)
#         pred_arr = res['data']
#         assert len(pred_arr[0]) == len(pred_arr[1])
