import json
import os.path as osp

import pytest

from objects.RServer import RServer

baseDir = osp.join('/', 'Robustar2').replace('\\', '/')
datasetDir = osp.join(baseDir, 'dataset').replace('\\', '/')
ckptDir = osp.join(baseDir, 'checkpoints').replace('\\', '/')
with open(osp.join(baseDir, 'configs.json')) as jsonfile:
    configs = json.load(jsonfile)

RServer.createServer(configs=configs, baseDir=baseDir, datasetDir=datasetDir, ckptDir=ckptDir)

def test_valid_app_and_server():
    server = RServer.getServer()
    assert server
    assert server.getFlaskApp()
    # assert server.dataManager
    # assert RServer.getModelWrapper()


@pytest.fixture()
def client():
    server = RServer.getServer()
    app = server.getFlaskApp()
    with app.test_client() as client:
        yield client


class TestPredict:

    def test_predict(self, client):
        rv = client.get("/backend_test/train/1")
        res = json.loads(rv.data)
        pred_arr = res['data']
        assert len(pred_arr[0]) == len(pred_arr[1])
