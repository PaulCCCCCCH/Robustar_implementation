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
    def test_edit_fail_invalid_split(self, client):
        rv = client.post("/edit/test/0").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Split test not supported! Currently we only support editing the `train` or `annotated` ' \
                            'splits!'

    def test_edit_fail_image_id_out_of_bound(self, client):
        # TODO: is it reasonable to test this function? if so, modify project code to pass the test
        rv = client.post("/edit/train/100000").get_json()  # TODO: error in `apis/edit.py` file line 67
        assert rv['code'] == -1
        # assert rv['msg'] == ''
        rv = client.post("/edit/annotate/100000").get_json()
        assert rv['code'] == -1
        # assert rv['msg'] == ''

    def test_edit_success(self, client):
        # TODO: is it reasonable to test this function? if so, modify project code to pass the test
        # TODO: may need a 'clean up' of file in folder `Robustar2/` - apply it in function `app()`
        rv = client.post("/edit/train/9").get_json()  # TODO: error in `apis/edit.py` file line 67
        assert rv['code'] == 0
        # TODO: test `bird/106.JPEG annotated, first row of /Robustar2/annotated.txt is 10`
        # TODO: more test cases ...

    def test_propose_fail_invalid_split(self, client):
        rv = client.get("/propose/test/0").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Cannot propose edit to a wrong split'

    def test_propose_fail_image_id_out_of_bound(self, client):  # TODO: modify project code to pass the test
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


class TestImage:
    def test_image_fail_invalid_split(self, client):
        rv = client.get("/image/non-exist/0").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Split not supported'

    def test_image_fail_image_id_out_of_bound(self, client):
        rv = client.get("/image/train/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'
        rv = client.get("/image/annotated/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'
        rv = client.get("/image/validation/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'
        rv = client.get("/image/proposed/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'
        rv = client.get("/image/test/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'
        rv = client.get("/image/validation_correct/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'
        rv = client.get("/image/validation_incorrect/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'
        rv = client.get("/image/test_correct/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'
        rv = client.get("/image/test_incorrect/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'

    def test_image_success(self, client):
        response = client.get("/image/train/2", follow_redirects=True)
        assert len(response.history) == 1  # Check that there was one redirect response
        assert response.request.path == "/dataset/Robustar2/dataset/train/bird/10.JPEG"
        response = client.get("/image/test/2", follow_redirects=True)
        assert len(response.history) == 1
        assert response.request.path == "/dataset/Robustar2/dataset/test/bird/10.JPEG"
        # TODO: test other <split>s (?)

    # TODO: GET /image/get-annotated/<image_id>

    def test_class_length_fail_invalid_split(self, client):
        rv = client.get("/image/class/non-exist").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Split not supported'

    def test_class_length_success(self, client):
        rv = client.get("/image/class/train").get_json()
        assert rv['code'] == 0
        assert rv['data'] == {'bird': 0, 'cat': 1000, 'crab': 2000, 'dog': 3000, 'fish': 4000, 'frog': 5000,
                              'insect': 6000, 'primate': 7000, 'turtle': 8000}
        # TODO: test other <split>s

    def test_split_length_fail_invalid_split(self, client):
        rv = client.get("/image/non-exist").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Split not supported'

    def test_split_length_success(self, client):
        rv = client.get("/image/train").get_json()
        assert rv['code'] == 0
        assert rv['data'] == 9000
        # TODO: test other <split>s


class TestPredict:
    def test_predict_fail_invalid_split(self, client):
        rv = client.get("/predict/non-exist/0").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Split not supported'

    def test_predict_fail_image_id_out_of_bound(self, client):
        rv = client.get("/predict/train/100000").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Image with given id not exist'
        # TODO: test other <split>s (?)

    def test_predict_success(self, client):
        rv = client.get("/predict/train/1").get_json()
        assert rv['code'] == 0
        data = rv['data']
        assert len(data[0]) == 9
        assert len(data[1]) == 9
        assert data[2] == ["/Robustar2/visualize_images/train_1_0.png",
                           "/Robustar2/visualize_images/train_1_1.png",
                           "/Robustar2/visualize_images/train_1_2.png",
                           "/Robustar2/visualize_images/train_1_3.png"]

# TODO: ...
