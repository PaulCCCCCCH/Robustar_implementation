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
    data_path = to_unix(request.config.getoption("data_path"))
    basedir = f"{data_path}-copy"

    _set_up(data_path, basedir)

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


def _set_up(data_path, basedir):
    if osp.exists(basedir):
        print(f"Remove {basedir}")
        shutil.rmtree(basedir)
    shutil.copytree(data_path, basedir)
    print(f"Copy {data_path} to {basedir}")


def _clean_up(basedir):
    shutil.rmtree(basedir)
    print(f"Remove {basedir}")
