import os
import os.path as osp
import shutil
import zipfile
import time

import pytest

from objects.RServer import RServer
from server import start_flask_app, new_server_object
from utils.path_utils import to_unix

PARAM_NAME_IMAGE_PATH = "image_url"


@pytest.fixture()
def app(request):
    zip_file_path = to_unix(request.config.getoption("zip_file_path"))
    basedir = zip_file_path[:-4]

    _set_up(zip_file_path)

    app, socket = start_flask_app()
    new_server_object(basedir, app, socket)
    server = RServer.get_server()
    app = server.get_flask_app()

    app.config["TESTING"] = True
    yield app
    app.config["TESTING"] = False

    server.get_data_manager().dispose_db_engine()
    _clean_up(basedir)

    time.sleep(0.1)


@pytest.fixture()
def client(app):
    yield app.test_client()


def _set_up(zip_file_path):
    root_dir = os.path.dirname(zip_file_path)
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(root_dir)
    print(f"Extracted {zip_file_path} to {root_dir}")


def _clean_up(basedir):
    shutil.rmtree(basedir)
    print(f"Remove {basedir}")
