import os
import os.path as osp
import threading

import pytest

from objects.RServer import RServer
from server import start_server
from utils.path_utils import to_unix


def test_valid_app_and_server():
    start_server()
    server = RServer.getServer()
    assert server
    assert server.getFlaskApp()


@pytest.fixture()
def app():
    _set_up()

    start_server()
    server = RServer.getServer()
    app = server.getFlaskApp()

    app.config['TESTING'] = True
    yield app
    app.config['TESTING'] = False

    _clean_up()

    # data_manager = server.getDataManager()
    # db_conn = data_manager.get_db_conn()
    # db_conn.close()  # TODO: [test] problematic, fail to use command line `pythom -m pytest`


def _set_up():
    base_dir = to_unix(osp.join('/', 'Robustar2'))

    # dataset_dir = to_unix(osp.join(base_dir, 'dataset'))
    # paired_path = to_unix(osp.join(dataset_dir, 'paired'))
    # if osp.exists(paired_path):
    #     print("cleanup > delete " + paired_path)
    #     for sub_folder in os.listdir(paired_path):
    #         sub_folder_root = to_unix(osp.join(paired_path, sub_folder))
    #         # print("cleanup >> delete " + sub_folder_root)
    #         for image in os.listdir(sub_folder_root):
    #             image_root = to_unix(osp.join(sub_folder_root, image))
    #             if os.path.isfile(image_root):
    #                 # print("cleanup >>> delete " + image_root)
    #                 os.remove(image_root)
    #         os.rmdir(sub_folder_root)
    #     os.rmdir(paired_path)
    #
    # db_path = to_unix(osp.join(base_dir, 'data.db'))
    # if osp.exists(db_path):
    #     print("cleanup > delete " + db_path)
    #     os.remove(db_path)

    dataset_dir = to_unix(osp.join(base_dir, 'dataset'))
    dataset_dir_original = to_unix(osp.join(base_dir, 'dataset_o'))
    os.rename(dataset_dir, dataset_dir_original)
    os.mkdir(dataset_dir)

    proposed_dir = to_unix(osp.join(base_dir, 'proposed'))
    proposed_dir_original = to_unix(osp.join(base_dir, 'proposed_o'))
    os.rename(proposed_dir, proposed_dir_original)
    os.mkdir(proposed_dir)

    visualize_images_dir = to_unix(osp.join(base_dir, 'visualize_images'))
    visualize_images_dir_original = to_unix(osp.join(base_dir, 'visualize_images_o'))
    os.rename(visualize_images_dir, visualize_images_dir_original)
    os.mkdir(visualize_images_dir)

    db_path = to_unix(osp.join(base_dir, 'data.db'))
    db_path_original = to_unix(osp.join(base_dir, 'data_o.db'))
    os.rename(db_path, db_path_original)
    open(db_path, 'a').close()


def _clean_up():
    base_dir = to_unix(osp.join('/', 'Robustar2'))

    dataset_dir = to_unix(osp.join(base_dir, 'dataset'))
    dataset_dir_original = to_unix(osp.join(base_dir, 'dataset_o'))
    os.rmdir(dataset_dir)
    os.rename(dataset_dir_original, dataset_dir)

    proposed_dir = to_unix(osp.join(base_dir, 'proposed'))
    proposed_dir_original = to_unix(osp.join(base_dir, 'proposed_o'))
    os.rmdir(proposed_dir)
    os.rename(proposed_dir_original, proposed_dir)

    visualize_images_dir = to_unix(osp.join(base_dir, 'visualize_images'))
    visualize_images_dir_original = to_unix(osp.join(base_dir, 'visualize_images_o'))
    os.rmdir(visualize_images_dir)
    os.rename(visualize_images_dir_original, visualize_images_dir)

    # db_path = to_unix(osp.join(base_dir, 'data.db'))
    # db_path_original = to_unix(osp.join(base_dir, 'data_o.db'))


@pytest.fixture()
def client(app):
    yield app.test_client()


# TODO: annotate 图片 逐像素位的检查
# TODO: test training


# Reserve 10 photos for each category in trainset and 10 photos for each category in testset to save time
class TestTrain:
    # Test if the model is loaded correctly at weight level
    def test_load_model_correctness(self, client, server):
        assert server.getModelsWeights() == {}

        data = {
            'info': 'placeholder',
            'configs': {
                'model_name': 'my-test-model',
                'weight': '',
                'train_path': '/Robustar2/dataset/train-2',
                'test_path': '/Robustar2/dataset/test-2',
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
                'epoch': 2,
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
        time.sleep(25)

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
                assert torch.equal(key_item_1[1], key_item_2[1])
