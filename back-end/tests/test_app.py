import pytest

from objects.RModelWrapper import RModelWrapper
from objects.RServer import RServer
from server import start_server

import os
import os.path as osp
import torch
import time

# start_server()
# def test_valid_app_and_server():
#     server = RServer.getServer()
#     assert server
#     assert server.getFlaskApp()
#     # assert server.dataManager
#     # assert RServer.getModelWrapper()


@pytest.fixture()
def app():
    _cleanup()
    start_server()
    server = RServer.getServer()
    app = server.getFlaskApp()
    app.config['TESTING'] = True
    yield app
    app.config['TESTING'] = False

@pytest.fixture()
def server():
    server = RServer.getServer()
    return server

def _cleanup():
    base_dir = osp.join('/', 'Robustar2').replace('\\', '/')
    dataset_dir = osp.join(base_dir, 'dataset').replace('\\', '/')
    test_correct_root = osp.join(dataset_dir, 'test_correct.txt').replace('\\', '/')
    test_incorrect_root = osp.join(dataset_dir, 'test_incorrect.txt').replace('\\', '/')
    validation_correct_root = osp.join(dataset_dir, 'validation_correct.txt').replace('\\', '/')
    validation_incorrect_root = osp.join(dataset_dir, 'validation_incorrect.txt').replace('\\', '/')
    annotated_root = osp.join(dataset_dir, 'annotated.txt').replace('\\', '/')
    paired_root = osp.join(dataset_dir, 'paired').replace('\\', '/')
    if osp.exists(test_correct_root):
        print("cleanup > delete " + test_correct_root)
        os.remove(test_correct_root)
    if osp.exists(test_incorrect_root):
        print("cleanup > delete " + test_incorrect_root)
        os.remove(test_incorrect_root)
    if osp.exists(validation_correct_root):
        print("cleanup > delete " + validation_correct_root)
        os.remove(validation_correct_root)
    if osp.exists(validation_incorrect_root):
        print("cleanup > delete " + validation_incorrect_root)
        os.remove(validation_incorrect_root)
    if osp.exists(annotated_root):
        print("cleanup > delete " + annotated_root)
        os.remove(annotated_root)
    if osp.exists(paired_root):
        print("cleanup > delete " + paired_root)
        for subfolder in os.listdir(paired_root):
            subfolder_root = osp.join(paired_root, subfolder).replace('\\', '/')
            print("cleanup >> delete " + subfolder_root)
            for image in os.listdir(subfolder_root):
                image_root = osp.join(subfolder_root, image).replace('\\', '/')
                if os.path.isfile(image_root):
                    # print("cleanup >>> delete " + image_root)
                    os.remove(image_root)
            os.rmdir(subfolder_root)
        os.rmdir(paired_root)


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

    def test_edit_fail_image_id_out_of_bound(self, client): # TODO: pass the test
        rv = client.post("/edit/train/100000").get_json()  # TODO: error in `apis/edit.py` file line 67
        assert rv['code'] == -1
        # assert rv['msg'] == ''
        rv = client.post("/edit/annotate/100000").get_json()
        assert rv['code'] == -1
        # assert rv['msg'] == ''

    def test_edit_success(self, client): # TODO: pass the test
        rv = client.post("/edit/train/9").get_json()  # TODO: error in `apis/edit.py` file line 67
        assert rv['code'] == 0
        # TODO: test `bird/106.JPEG annotated, first row of /Robustar2/annotated.txt is 10`
        # TODO: more test cases ...

    def test_propose_fail_invalid_split(self, client):
        rv = client.get("/propose/test/0").get_json()
        assert rv['code'] == -1
        assert rv['msg'] == 'Cannot propose edit to a wrong split'

    def test_propose_fail_image_id_out_of_bound(self, client):  # TODO: pass the test
        rv = client.get("/propose/train/100000").get_json()
        assert rv['code'] == -1
        # assert rv['msg'] == ''
        rv = client.get("/propose/annotate/100000").get_json()
        assert rv['code'] == -1
        # assert rv['msg'] == ''

    def test_propose_success(self, client):
        rv = client.get("/propose/train/9").get_json()
        assert rv['code'] == 0
        # TODO: test `bird/106.JPEG annotated, first row of /Robustar2/annotated.txt is 10`
        # TODO: more test cases ...

    def test_auto_annotate_success(self, client):
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
        # TODO: test other <split>s

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

# TODO: annotate 图片 逐像素位的检查
# TODO: test training


# Reserve 3 photos for each category in trainset and 10 photos for each category in testset to save time
class TestTrain:
    # Test if the model is loaded correctly at weight level
    def test_load_model_correctness(self, client, server):
        assert server.getModelsWeights() == {}

        data = {
            'info': 'placeholder',
            'configs': {
                            'model_name': 'my-test-model',
                            'weight': '',
                            'train_path': '/Robustar2/dataset/train-origin',
                            'test_path': '/Robustar2/dataset/test-origin',
                            'class_path': './model/cifar-class.txt',
                            'port': '8000',
                            'save_dir': '/Robustar2/checkpoints',
                            'use_paired_train': False,
                            'mixture': 'random_pure',
                            'paired_data_path': '/Robustar2/dataset/paired',
                            'auto_save_model': True,
                            'batch_size': '128',
                            'shuffle': True,
                            'learn_rate': 0.1,
                            'pgd': 'no PGD',
                            'paired_train_reg_coeff': 0.001,
                            'image_size': 32,
                            'epoch': 3,
                            'thread': 8,
                            'pretrain': False,
                            'user_edit_buffering': False,
                            'save_every': 1
            }
        }

        rv = client.post("/train", json=data).get_json()
        assert rv['code'] == 0
        assert rv['data'] == 'Training started!'
        assert rv['msg'] == 'Success'

        # Wait for the training
        time.sleep(90)

        # Compare model weights saved in local path and in memory
        for name, weight in server.getModelsWeights().items():
            # Get the model weights saved in local path
            model_arch = server.getServerConfigs()['model_arch']
            net_path = os.path.join(server.ckptDir, name).replace('\\', '/')
            device = server.getServerConfigs()['device']
            pre_trained = server.getServerConfigs()['pre_trained']
            num_classes = server.getServerConfigs()['num_classes']
            modelWrapper = RModelWrapper(model_arch, net_path, device, pre_trained, num_classes)
            modelLoaded = modelWrapper.model
            weightLoaded = modelLoaded.state_dict()

            # Get the model weights saved in memory
            weightInMem = server.getModelsWeights()[name]

            # Compare each item in them
            for key_item_1, key_item_2 in zip(weightLoaded.items(), weightInMem.items()):
                # Skip the comparing of running_mean and running_var in BN layers
                if ('running' in key_item_1[0]):
                    continue
                if(torch.equal(key_item_1[1], key_item_2[1]) == False):
                    print(key_item_1)
                    print(key_item_2)
                assert torch.equal(key_item_1[1], key_item_2[1])
