from .edit import edit_api
from .generate import generate_api
from .image import image_api
from .predict import predict_api
from .train import train_api
from .test import test_api
from .config import config_api
from .task import task_api

blueprints = [
    edit_api,
    generate_api,
    image_api,
    predict_api,
    train_api,
    test_api,
    config_api,
    task_api,
]
