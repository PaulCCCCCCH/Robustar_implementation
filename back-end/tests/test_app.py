import pytest

from objects.RServer import RServer
from server import start_server

start_server()


def test_valid_app_and_server():
    server = RServer.getServer()
    assert server
    assert server.getFlaskApp()
    # assert server.dataManager
    # assert RServer.getModelWrapper()


@pytest.fixture()
def app():
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


class TestEdit:
    def test_edit_wrong_split(self, client):
        rv = client.post("/edit/test/0").get_data()
        assert rv == -1

# class TestPredict:
#
#     def test_predict(self, client):
#         rv = client.get("/backend_test/train/1")
#         res = json.loads(rv.data)
#         pred_arr = res['data']
#         assert len(pred_arr[0]) == len(pred_arr[1])
