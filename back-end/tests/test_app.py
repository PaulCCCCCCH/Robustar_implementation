import os
import os.path as osp
import shutil
import time

import pytest

from objects.RServer import RServer
from server import start_flask_app, new_server_object
from utils.path_utils import to_unix

PARAM_NAME_IMAGE_PATH = "image_url"


@pytest.fixture()
def app(request):
    basedir = request.config.getoption("basedir")
    app = None
    try:
        _set_up(basedir)

        if app is None:
            app, _ = start_flask_app()
            server = new_server_object(basedir)
            server = RServer.get_server()
            app = server.get_flask_app()

        app.config["TESTING"] = True
        yield app
        app.config["TESTING"] = False

    except Exception as e:
        _clean_up(basedir)
        raise e

    time.sleep(0.1)


@pytest.fixture()
def client(app):
    yield app.test_client()


def _set_up(basedir):
    # print(os.getcwd())
    base_dir = to_unix(basedir)

    dataset_dir = to_unix(osp.join(base_dir, "dataset"))
    dataset_dir_original = to_unix(osp.join(base_dir, "dataset_o"))
    if osp.exists(dataset_dir):
        os.rename(dataset_dir, dataset_dir_original)
        os.mkdir(dataset_dir)
        print("setup > rename " + dataset_dir + " to " + dataset_dir_original)
        train_dir = to_unix(osp.join(dataset_dir, "train"))
        train_dir_original = to_unix(osp.join(dataset_dir_original, "train"))
        os.mkdir(train_dir)
        for name in os.listdir(train_dir_original):
            image_dir = to_unix(osp.join(train_dir, name))
            image_dir_original = to_unix(osp.join(train_dir_original, name))
            if not osp.isdir(image_dir_original):
                # if len(image_dir.split('/')[-1].split('.')) > 1:
                continue
            os.mkdir(image_dir)
            for i in range(10):
                image = to_unix(osp.join(image_dir, "{}.JPEG".format(i)))
                image_original = to_unix(
                    osp.join(image_dir_original, "{}.JPEG".format(i))
                )
                shutil.copy2(image_original, image)
        print("setup >> test train set created")
        test_dir = to_unix(osp.join(dataset_dir, "test"))
        test_dir_original = to_unix(osp.join(dataset_dir_original, "test"))
        os.mkdir(test_dir)
        for name in os.listdir(test_dir_original):
            image_dir = to_unix(osp.join(test_dir, name))
            image_dir_original = to_unix(osp.join(test_dir_original, name))
            if not osp.isdir(image_dir_original):
                # if len(image_dir.split('/')[-1].split('.')) > 1:
                continue
            os.mkdir(image_dir)
            for i in range(10):
                image = to_unix(osp.join(image_dir, "{}.JPEG".format(i)))
                image_original = to_unix(
                    osp.join(image_dir_original, "{}.JPEG".format(i))
                )
                shutil.copy2(image_original, image)
        print("setup >> test test set created")
        validation_dir = to_unix(osp.join(dataset_dir, "validation"))
        os.mkdir(validation_dir)
        for name in os.listdir(test_dir_original):
            image_dir = to_unix(osp.join(validation_dir, name))
            image_dir_original = to_unix(osp.join(test_dir_original, name))
            if not osp.isdir(image_dir_original):
                continue
            os.mkdir(image_dir)
            for i in range(10, 20):
                image = to_unix(osp.join(image_dir, "{}.JPEG".format(i)))
                image_original = to_unix(
                    osp.join(image_dir_original, "{}.JPEG".format(i))
                )
                shutil.copy2(image_original, image)
        print("setup >> test validation set created")
        print("setup > copy images into " + dataset_dir)
    else:
        print("setup > no database dir, skip copy")

    proposed_dir = to_unix(osp.join(base_dir, "proposed"))
    proposed_dir_original = to_unix(osp.join(base_dir, "proposed_o"))
    if osp.exists(proposed_dir):
        os.rename(proposed_dir, proposed_dir_original)
        os.mkdir(proposed_dir)
        print("setup > rename " + proposed_dir + " to " + proposed_dir_original)
        for name in os.listdir(proposed_dir_original):
            image_dir = to_unix(osp.join(proposed_dir, name))
            os.mkdir(image_dir)
            image_dir_original = to_unix(osp.join(proposed_dir_original, name))
            for i in range(10):
                image = to_unix(osp.join(image_dir, "{}.JPEG".format(i)))
                image_original = to_unix(
                    osp.join(image_dir_original, "{}.JPEG".format(i))
                )
                shutil.copy2(image_original, image)
        print("setup > copy images into " + proposed_dir)
    else:
        print("setup > no proposed dir, skip copy")

    db_path = to_unix(osp.join(base_dir, "data.db"))
    if osp.exists(db_path):
        print("setup > delete " + db_path)
        os.remove(db_path)
    else:
        print("setup > no db, skip delete")

    visualize_images_dir = to_unix(osp.join(base_dir, "visualize_images"))
    if osp.exists(visualize_images_dir):
        for name in os.listdir(visualize_images_dir):
            image_path = to_unix(osp.join(visualize_images_dir, name))
            os.remove(image_path)
        print("setup > delete " + visualize_images_dir)
    else:
        print("setup > no visualize images dir, skip delete")

    # db_path = to_unix(osp.join(base_dir, 'data.db'))
    # db_path_original = to_unix(osp.join(base_dir, 'data_o.db'))
    # os.rename(db_path, db_path_original)
    # open(db_path, 'a').close()


def _clean_up(basedir):
    base_dir = to_unix(basedir)

    dataset_dir = to_unix(osp.join(base_dir, "dataset"))
    dataset_dir_original = to_unix(osp.join(base_dir, "dataset_o"))
    if osp.exists(dataset_dir_original):
        for split in os.listdir(dataset_dir):
            split_dir = to_unix(osp.join(dataset_dir, split))
            for class_name in os.listdir(split_dir):
                class_name_dir = to_unix(osp.join(split_dir, class_name))
                for image_name in os.listdir(class_name_dir):
                    img = to_unix(osp.join(class_name_dir, image_name))
                    os.remove(img)
                os.rmdir(class_name_dir)
            os.rmdir(split_dir)
        os.rmdir(dataset_dir)
        os.rename(dataset_dir_original, dataset_dir)
        print("cleanup > switch " + dataset_dir_original + " to " + dataset_dir)
    else:
        print("cleanup > no origin database dir, skip restore")

    proposed_dir = to_unix(osp.join(base_dir, "proposed"))
    proposed_dir_original = to_unix(osp.join(base_dir, "proposed_o"))
    if osp.exists(proposed_dir_original):
        for class_name in os.listdir(proposed_dir):
            class_name_dir = to_unix(osp.join(proposed_dir, class_name))
            for image_name in os.listdir(class_name_dir):
                img = to_unix(osp.join(class_name_dir, image_name))
                os.remove(img)
            os.rmdir(class_name_dir)
        os.rmdir(proposed_dir)
        os.rename(proposed_dir_original, proposed_dir)
        print("cleanup > switch " + proposed_dir_original + " to " + proposed_dir)
    else:
        print("cleanup > no origin proposed dir, skip restore")

    # proposed_dir = to_unix(osp.join(base_dir, 'proposed'))
    # proposed_dir_original = to_unix(osp.join(base_dir, 'proposed_o'))
    # os.rmdir(proposed_dir)
    # os.rename(proposed_dir_original, proposed_dir)
    #
    # visualize_images_dir = to_unix(osp.join(base_dir, 'visualize_images'))
    # visualize_images_dir_original = to_unix(osp.join(base_dir, 'visualize_images_o'))
    # os.rmdir(visualize_images_dir)
    # os.rename(visualize_images_dir_original, visualize_images_dir)

    db_path = to_unix(osp.join(base_dir, "data.db"))
    if osp.exists(db_path):
        print("cleanup > delete " + db_path)
        os.remove(db_path)
    else:
        print("cleanup > no db, skip delete")

    # db_path = to_unix(osp.join(base_dir, 'data.db'))
    # db_path_original = to_unix(osp.join(base_dir, 'data_o.db'))


# Reserve 10 photos for each category in trainset and 10 photos for each category in testset to save time
# class TestTrain:
#     # Test if the model is loaded correctly at weight level
#     def test_load_model_correctness(self, client, server):
#         assert server.get_model_weights() == {}
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
#         for name, weight in server.get_model_weights().items():
#             # Get the model weights saved in local path
#             model_arch = server.get_server_configs()['model_arch']
#             net_path = os.path.join(server.ckpt_dir, name).replace('\\', '/')
#             device = server.get_server_configs()['device']
#             pre_trained = server.get_server_configs()['pre_trained']
#             num_classes = server.get_server_configs()['num_classes']
#             model_wrapper = RModelWrapper(model_arch, net_path, device, pre_trained, num_classes)
#             modelLoaded = model_wrapper.model
#             weightLoaded = modelLoaded.state_dict()
#
#             # Get the model weights saved in memory
#             weightInMem = server.get_model_weights()[name]
#
#             # Compare each item in them
#             for key_item_1, key_item_2 in zip(weightLoaded.items(), weightInMem.items()):
#                 assert torch.equal(key_item_1[1], key_item_2[1])
