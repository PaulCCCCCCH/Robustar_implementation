import os
import os.path as osp
import shutil
import time

import pytest

from objects.RServer import RServer
from server import start_server
from utils.path_utils import to_unix

PARAM_NAME_IMAGE_PATH = "image_url"


@pytest.fixture()
def app(request):
    basedir = request.config.getoption("basedir")

    _set_up(basedir)

    start_server(basedir)
    server = RServer.getServer()
    app = server.getFlaskApp()

    app.config['TESTING'] = True
    yield app
    app.config['TESTING'] = False

    RServer.getDataManager().get_db_conn().close()
    # due to unavailability of close_connection() in fs.py

    _clean_up(basedir)

    time.sleep(0.1)


@pytest.fixture()
def client(app):
    yield app.test_client()


def _set_up(basedir):
    # print(os.getcwd())
    base_dir = to_unix(basedir)

    dataset_dir = to_unix(osp.join(base_dir, 'dataset'))
    dataset_dir_original = to_unix(osp.join(base_dir, 'dataset_o'))
    if osp.exists(dataset_dir):
        os.rename(dataset_dir, dataset_dir_original)
        os.mkdir(dataset_dir)
        print("setup > rename " + dataset_dir + " to " + dataset_dir_original)
        train_dir = to_unix(osp.join(dataset_dir, 'train'))
        train_dir_original = to_unix(osp.join(dataset_dir_original, 'train'))
        os.mkdir(train_dir)
        for name in os.listdir(train_dir_original):
            image_dir = to_unix(osp.join(train_dir, name))
            image_dir_original = to_unix(osp.join(train_dir_original, name))
            if not osp.isdir(image_dir_original):
                continue
            os.mkdir(image_dir)
            for i in range(10):
                image = to_unix(osp.join(image_dir, "{}.JPEG".format(i)))
                image_original = to_unix(osp.join(image_dir_original, "{}.JPEG".format(i)))
                shutil.copy2(image_original, image)
        print("setup >> test train set created")
        test_dir = to_unix(osp.join(dataset_dir, 'test'))
        test_dir_original = to_unix(osp.join(dataset_dir_original, 'test'))
        os.mkdir(test_dir)
        for name in os.listdir(test_dir_original):
            image_dir = to_unix(osp.join(test_dir, name))
            image_dir_original = to_unix(osp.join(test_dir_original, name))
            if not osp.isdir(image_dir_original):
                continue
            os.mkdir(image_dir)
            for i in range(10):
                image = to_unix(osp.join(image_dir, "{}.JPEG".format(i)))
                image_original = to_unix(osp.join(image_dir_original, "{}.JPEG".format(i)))
                shutil.copy2(image_original, image)
        print("setup >> test test set created")
        validation_dir = to_unix(osp.join(dataset_dir, 'validation'))
        os.mkdir(validation_dir)
        for name in os.listdir(test_dir_original):
            image_dir = to_unix(osp.join(validation_dir, name))
            image_dir_original = to_unix(osp.join(test_dir_original, name))
            if not osp.isdir(image_dir_original):
                continue
            os.mkdir(image_dir)
            for i in range(10, 20):
                image = to_unix(osp.join(image_dir, "{}.JPEG".format(i)))
                image_original = to_unix(osp.join(image_dir_original, "{}.JPEG".format(i)))
                shutil.copy2(image_original, image)
        print("setup >> test validation set created")
        print("setup > copy images into " + dataset_dir)
    else:
        print("setup > no database dir, skip copy")

    # create generated folder
    generated_folder = osp.join(base_dir, "generated")
    if not osp.exists(generated_folder):
        os.mkdir(generated_folder)

    proposed_dir = to_unix(osp.join(base_dir, "generated", 'proposed'))
    proposed_dir_original = to_unix(osp.join(base_dir, "generated", 'proposed_o'))
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
                image_original = to_unix(osp.join(image_dir_original, "{}.JPEG".format(i)))
                shutil.copy2(image_original, image)
        print("setup > copy images into " + proposed_dir)
    else:
        print("setup > no proposed dir, skip copy")

    db_path = to_unix(osp.join(base_dir, "generated", 'data.db'))
    if osp.exists(db_path):
        print("setup > delete " + db_path)
        os.remove(db_path)
    else:
        print("setup > no db, skip delete")

    visualize_images_dir = to_unix(osp.join(base_dir, "generated", 'visualize_images'))
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

    dataset_dir = to_unix(osp.join(base_dir, 'dataset'))
    dataset_dir_original = to_unix(osp.join(base_dir, 'dataset_o'))
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

    proposed_dir = to_unix(osp.join(base_dir, "generated", 'proposed'))
    proposed_dir_original = to_unix(osp.join(base_dir, "generated", 'proposed_o'))
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

    db_path = to_unix(osp.join(base_dir, "generated", 'data.db'))
    if osp.exists(db_path):
        print("cleanup > delete " + db_path)
        os.remove(db_path)
    else:
        print("cleanup > no db, skip delete")

    # db_path = to_unix(osp.join(base_dir, 'data.db'))
    # db_path_original = to_unix(osp.join(base_dir, 'data_o.db'))


