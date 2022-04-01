import pytest

from objects.RServer import RServer
from server import start_server


# start_server()
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
    def test_config_success(self, client):
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
    def test_edit_fail_wrong_split(self, client):
        rv = client.post("/edit/test/0").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Split test not supported! Currently we only support editing the `train` or `annotated` ' \
                            'splits!'

    def test_edit_fail_image_id_out_of_bound(self, client):
        # TODO: is it reasonable to test this function? if so, make this test pass
        rv = client.post("/edit/train/100000").get_json()  # TODO: error in `apis/edit.py` file line 67
        assert rv['code'] == -1
        # assert rv['msg'] == ''
        rv = client.post("/edit/annotate/100000").get_json()
        assert rv['code'] == -1
        # assert rv['msg'] == ''

    def test_edit_success(self, client):
        # TODO: is it reasonable to test this function? if so, make this test pass
        # TODO: may need a 'clean up' of file in folder `Robustar2/` - apply it in function `app()`
        rv = client.post("/edit/train/9").get_json()  # TODO: error in `apis/edit.py` file line 67
        assert rv['code'] == 0
        # TODO: test `bird/106.JPEG annotated, first row of /Robustar2/annotated.txt is 10`
        # TODO: more test cases ...

    def test_propose_fail_wrong_split(self, client):
        rv = client.get("/propose/test/0").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Cannot propose edit to a wrong split'

    def test_propose_fail_image_id_out_of_bound(self, client):  # TODO: make this test pass
        rv = client.get("/propose/train/100000").get_json()
        assert rv['code'] == -1
        # assert rv['msg'] == ''
        rv = client.get("/propose/annotate/100000").get_json()
        assert rv['code'] == -1
        # assert rv['msg'] == ''

    def test_propose_success(self, client):
        # TODO: may need a 'clean up' of file in folder `Robustar2/` - apply it in function `app()`
        rv = client.get("/propose/train/9").get_json()
        assert rv['code'] == 0
        # TODO: test `bird/106.JPEG annotated, first row of /Robustar2/annotated.txt is 10`
        # TODO: more test cases ...

    def test_auto_annotate_success(self, client):
        # TODO: may need a 'clean up' of file in folder `Robustar2/` - apply it in function `app()`
        assert True  # TODO: test not implemented

    # TODO: tests on auto_annotate not implemented

# class TestPredict:
#
#     def test_predict(self, client):
#         rv = client.get("/backend_test/train/1")
#         res = json.loads(rv.data)
#         pred_arr = res['data']
#         assert len(pred_arr[0]) == len(pred_arr[1])
