import os
import os.path as osp
import shutil
import time
import zipfile

import pytest

from objects.RServer import RServer
from server import start_flask_app, new_server_object
from utils.path_utils import to_unix
from database.db_init import db

PARAM_NAME_IMAGE_PATH = "image_url"
flask_app = None


@pytest.fixture(scope="function")
def app(request):
    global flask_app
    basedir = to_unix(request.config.getoption("basedir"))
    try:
        _set_up(basedir)

        if flask_app is None:
            flask_app, _ = start_flask_app()
            new_server_object(to_unix(os.path.join(basedir, "Robustar2-test")))
            server = RServer.get_server()
            flask_app = server.get_flask_app()

        flask_app.config["TESTING"] = True
        yield flask_app
        flask_app.config["TESTING"] = False

        # Clean up the database resources
        with flask_app.app_context():
            db.session.remove()
            db.engine.dispose()

    except Exception as e:
        _clean_up(basedir)
        raise e
    finally:
        _clean_up(basedir)

    time.sleep(0.1)


@pytest.fixture(scope="function")
def client(app):
    yield app.test_client()


def _set_up(basedir):
    # Unzip dataset from Robustar2-test.zip
    zip_file_path = to_unix(osp.join(basedir, "Robustar2-test.zip"))

    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(basedir)
    except Exception as e:
        raise Exception(f"Failed to extract {zip_file_path} to {basedir}.")
        print(e)
    print(f"Extracted {zip_file_path} to {basedir}")


def _clean_up(basedir):
    dataset_dir = to_unix(osp.join(basedir, "Robustar2-test"))
    shutil.rmtree(dataset_dir)
    print(f"Remove {dataset_dir}")
