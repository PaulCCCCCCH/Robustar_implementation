from objects.RServer import RServer
from objects.RDataManager import RDataManager
import pytest
import json

from server import create_server

create_server()

def test_valid_app_and_server():
    server = RServer.getServer()
    assert server
    assert server.getFlaskApp()
    assert server.dataManager 
    assert RServer.getModelWrapper()

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
        assert len(pred_arr[0])==len(pred_arr[1])
    

