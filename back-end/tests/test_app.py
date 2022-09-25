import os
import os.path as osp
import shutil
import threading

import pytest

from objects.RServer import RServer
from server import start_server
from utils.path_utils import to_unix


# def test_valid_app_and_server():
#     start_server()
#     server = RServer.getServer()
#     assert server
#     assert server.getFlaskApp()

@pytest.fixture()
def app(request):
    basedir = request.config.getoption("basedir")
    _cleanup(basedir)
    start_server(basedir)
    server = RServer.getServer()
    app = server.getFlaskApp()

    app.config['TESTING'] = True
    yield app
    app.config['TESTING'] = False

    _clean_up()

def _cleanup(basedir):
    base_dir = basedir.replace('\\', '/')
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

    # db_path = to_unix(osp.join(base_dir, 'data.db'))
    # if osp.exists(db_path):
    #     print("cleanup > delete " + db_path)
    #     os.remove(db_path)

    # dataset_dir = to_unix(osp.join(base_dir, 'dataset'))
    # dataset_dir_original = to_unix(osp.join(base_dir, 'dataset_o'))
    # os.rename(dataset_dir, dataset_dir_original)
    # os.mkdir(dataset_dir)
    # test_dir = to_unix(osp.join(dataset_dir, 'test'))
    # test_dir_original = to_unix(osp.join(dataset_dir_original, 'test'))
    # os.mkdir(test_dir)
    # dog_dir = to_unix(osp.join(test_dir, 'dog'))
    # dog_dir_original = to_unix(osp.join(test_dir_original, 'dog'))
    # os.mkdir(dog_dir)
    # for i in range(10):
    #     dog_img = to_unix(osp.join(dog_dir, str(i) + '.JPEG'))
    #     dog_img_original = to_unix(osp.join(dog_dir_original, str(i) + '.JPEG'))
    #     shutil.copyfile(dog_img_original, dog_img)

    # proposed_dir = to_unix(osp.join(base_dir, 'proposed'))
    # proposed_dir_original = to_unix(osp.join(base_dir, 'proposed_o'))
    # os.rename(proposed_dir, proposed_dir_original)
    # os.mkdir(proposed_dir)
    #
    # visualize_images_dir = to_unix(osp.join(base_dir, 'visualize_images'))
    # visualize_images_dir_original = to_unix(osp.join(base_dir, 'visualize_images_o'))
    # os.rename(visualize_images_dir, visualize_images_dir_original)
    # os.mkdir(visualize_images_dir)
    #
    # db_path = to_unix(osp.join(base_dir, 'data.db'))
    # db_path_original = to_unix(osp.join(base_dir, 'data_o.db'))
    # os.rename(db_path, db_path_original)
    # open(db_path, 'a').close()


def _clean_up():
    pass

    # base_dir = to_unix(osp.join('/', 'Robustar2'))
    #
    # dataset_dir = to_unix(osp.join(base_dir, 'dataset'))
    # dataset_dir_original = to_unix(osp.join(base_dir, 'dataset_o'))
    # os.rmdir(dataset_dir)
    # os.rename(dataset_dir_original, dataset_dir)

    # proposed_dir = to_unix(osp.join(base_dir, 'proposed'))
    # proposed_dir_original = to_unix(osp.join(base_dir, 'proposed_o'))
    # os.rmdir(proposed_dir)
    # os.rename(proposed_dir_original, proposed_dir)
    #
    # visualize_images_dir = to_unix(osp.join(base_dir, 'visualize_images'))
    # visualize_images_dir_original = to_unix(osp.join(base_dir, 'visualize_images_o'))
    # os.rmdir(visualize_images_dir)
    # os.rename(visualize_images_dir_original, visualize_images_dir)

    # db_path = to_unix(osp.join(base_dir, 'data.db'))
    # db_path_original = to_unix(osp.join(base_dir, 'data_o.db'))


@pytest.fixture()
def client(app):
    yield app.test_client()


# Reserve 10 photos for each category in trainset and 10 photos for each category in testset to save time
# class TestTrain:
#     # Test if the model is loaded correctly at weight level
#     def test_load_model_correctness(self, client, server):
#         assert server.getModelsWeights() == {}
#
#         data = {
#             'info': 'placeholder',
#             'configs': {
#                 'model_name': 'my-test-model',
#                 'weight': '',
#                 'train_path': '/Robustar2/dataset/train-2',
#                 'test_path': '/Robustar2/dataset/test-2',
#                 'class_path': './model/cifar-class.txt',
#                 'port': '8000',
#                 'save_dir': '/Robustar2/checkpoints',
#                 'use_paired_train': False,
#                 'mixture': 'random_pure',
#                 'paired_data_path': '/Robustar2/dataset/paired',
#                 'auto_save_model': True,
#                 'batch_size': '128',
#                 'shuffle': True,
#                 'learn_rate': 0.1,
#                 'pgd': 'no PGD',
#                 'paired_train_reg_coeff': 0.001,
#                 'image_size': 32,
#                 'epoch': 2,
#                 'thread': 8,
#                 'pretrain': False,
#                 'user_edit_buffering': False,
#                 'save_every': 1
#             }
#         }
#
#         rv = client.post("/train", json=data).get_json()
#         assert rv['code'] == 0
#         assert rv['data'] == 'Training started!'
#         assert rv['msg'] == 'Success'
#
#         # Wait for the training
#         time.sleep(25)
#
#         # Compare model weights saved in local path and in memory
#         for name, weight in server.getModelsWeights().items():
#             # Get the model weights saved in local path
#             model_arch = server.getServerConfigs()['model_arch']
#             net_path = os.path.join(server.ckptDir, name).replace('\\', '/')
#             device = server.getServerConfigs()['device']
#             pre_trained = server.getServerConfigs()['pre_trained']
#             num_classes = server.getServerConfigs()['num_classes']
#             modelWrapper = RModelWrapper(model_arch, net_path, device, pre_trained, num_classes)
#             modelLoaded = modelWrapper.model
#             weightLoaded = modelLoaded.state_dict()
#
#             # Get the model weights saved in memory
#             weightInMem = server.getModelsWeights()[name]
#
#             # Compare each item in them
#             for key_item_1, key_item_2 in zip(weightLoaded.items(), weightInMem.items()):
#                 assert torch.equal(key_item_1[1], key_item_2[1])

