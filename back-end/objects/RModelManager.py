import torch
import torchvision
import os
from threading import Lock
from flask_sqlalchemy import SQLAlchemy
from database.model import *

IMAGENET_OUTPUT_SIZE = 1000

MODEL_INPUT_SHAPE = {
    "resnet-18": 224,
    "resnet-34": 224,
    "resnet-50": 224,
    "resnet-101": 224,
    "resnet-152": 224,
    "mobilenet-v2": 224,
    "resnet-18-32x32": 32,
    "alexnet": 227,
}

# TODO(Chonghan): Change this class to RModelManager later.
class RModelManager:
    def __init__(
        self, db_conn, device
    ):
        self.db_conn: SQLAlchemy = db_conn

        self.device = device  # We keep device as string to allow for easy comparison
        self._lock = Lock()
        self._model_available = True
        self.model = None

    def acquire_model(self):
        """
        A thread-safe way to acquire access to the model. This is to make sure that only one
        thread can own the model at a time to avoid conflicts in gradient calculation. Always call
        this function before using the model (e.g., training, inferencing, ...)

        Return True if the model is available, False otherwise.
        """
        self._lock.acquire()

        if self._model_available:
            self._model_available = False
            self._lock.release()
            return True

        self._lock.release()
        return False

    def release_model(self):
        """
        Release the model so that other threads can use it
        """
        self._lock.acquire()
        self._model_available = True
        self._lock.release()

    def create_model(self, fields: dict):
        # TODO: Need to validate fields, dump model definition to a file,
        # etc. Either do these here or somewhere else

        tags = fields.pop('tags', [])

        tag_objs = []
        if tags:
            for tag_name in tags:
                tag = self.db_conn.session.query(Tags).filter_by(name=tag_name).first()
                if tag is None:
                    tag = Tags(name=tag_name)
                    self.db_conn.session.add(tag)
                tag_objs.append(tag)

        model = Models(**fields, tags=tag_objs)
        self.db_conn.session.add(model)
        self.db_conn.session.commit()

    def list_models(self) -> Models:
        return Models.query.all()

    def delete_model_by_nickname(self, nickname):
        model_to_delete = Models.query.filter_by(nickname=nickname).first()
        if model_to_delete:
            db.session.delete(model_to_delete)
            db.session.commit()
        else:
            print(
                f"Attempting to delete a model that does not exist. Model name: {nickname}"
            )

    def get_model_by_nickname(self, nickname):
        return Models.query.filter_by(nickname=nickname).first()

    # Function to convert a model object to a dictionary
    def convert_model_2_dict(self, model_record):
        data = {c.name: getattr(model_record, c.name) for c in model_record.__table__.columns}
        data["tags"] = [tag.name for tag in model_record.tags]
        # influences currently not considered
        return data
