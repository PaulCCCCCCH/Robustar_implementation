import shutil
import time
import pytest

from objects.RServer import RServer
from server import start_flask_app, new_server_object
from database.db_init import db

from utils.path_utils import to_unix


def pytest_addoption(parser):
    parser.addoption(
        "--data_path",
        action="store",
        default="/Robustar2-test",
        help="Path of the test data",
    )


@pytest.fixture(scope="function")
def client(request):
    data_path = to_unix(request.config.getoption("data_path"))
    basedir = f"{data_path}-copy"

    _set_up(data_path, basedir)

    app, socket = start_flask_app()
    new_server_object(basedir, app, socket)
    server = RServer.get_server()
    app = server.get_flask_app()

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        with app.app_context():
            db.session.commit()
            db.create_all()
            yield test_client
            db.session.commit()
            db.drop_all()

    app.config["TESTING"] = False

    server.get_data_manager().dispose_db_engine()
    _clean_up(basedir)

    time.sleep(0.1)


def _set_up(data_path, basedir):
    shutil.copytree(data_path, basedir, dirs_exist_ok=True)
    print(f"Copy {data_path} to {basedir}")


def _clean_up(basedir):
    shutil.rmtree(basedir, ignore_errors=True)
    print(f"Remove {basedir}")
