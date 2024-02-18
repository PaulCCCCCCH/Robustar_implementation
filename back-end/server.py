import json
import os.path as osp
import os
from objects.RServer import RServer
from objects.RDataManager import RDataManager
from objects.RModelWrapper import RModelWrapper, MODEL_INPUT_SHAPE
from objects.RAutoAnnotator import RAutoAnnotator
from utils.path_utils import to_unix, to_absolute
from utils.predict import get_image_prediction
from flask import Flask
import argparse
from flask_socketio import emit, SocketIO
from apis import blueprints
import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.WARNING)


def start_flask_app():
    def after_request(resp):
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Headers"] = "*"
        return resp

    app = Flask(__name__)
    app.after_request(after_request)

    # register all api routes
    for bp in blueprints:
        # TODO: use /api/<version> prefix
        # app.register_blueprint(bp, url_prefix='/api/v1')
        app.register_blueprint(bp)

    socket = SocketIO(app, cors_allowed_origins="*")

    return app, socket


# Get server listener objects
app, socket = start_flask_app()


# Init socket connection
@socket.on("connect")
def test_connect():
    print("Successfully connected to frontend with socket")
    emit("afterConnect", {"data": "Lets dance"})


def precheck():
    configs = RServer.get_server_configs()
    data_manager = RServer.get_data_manager()
    model_wrapper = RServer.get_model_wrapper()
    trainset = data_manager.trainset
    testset = data_manager.testset
    validationset = data_manager.validationset

    def check_num_classes_consistency():
        classes_num = configs["num_classes"]
        error_template = "Number of classes specified in configs.json({}) doesn't match that in dataset {}({})"
        errors = []
        if len(trainset.classes) != classes_num:
            errors.append(
                error_template.format(
                    classes_num, "Training Set", len(trainset.classes)
                )
            )
        if len(testset.classes) != classes_num:
            errors.append(
                error_template.format(classes_num, "Test Set", len(trainset.classes))
            )
        if len(validationset.classes) != classes_num:
            errors.append(
                error_template.format(
                    classes_num, "Validation Set", len(trainset.classes)
                )
            )
        assert len(errors) == 0, "\n".join(errors)

    def check_image_size_consistency():
        try:
            get_image_prediction(
                model_wrapper, trainset.get_image_list()[0], data_manager.image_size
            )
        except Exception as e:
            mapping = [f"{model}: {size}" for model, size in MODEL_INPUT_SHAPE.items()]
            print(
                f"""
            Image size consistency check failed. This is likely to be caused by a mismatch between image_size and model architecture configurations. Different models require input images of different sizes.
            The mapping is {mapping}
            \n
            raw error message: {(e)}
            """
            )
            raise

    check_num_classes_consistency()
    check_image_size_consistency()


def new_server_object(base_dir, app, socket):
    base_dir = to_unix(base_dir)
    dataset_dir = to_unix(osp.join(base_dir, "dataset"))
    ckpt_dir = to_unix(osp.join(base_dir, "checkpoints"))
    db_path = to_unix(osp.join(base_dir, "data.db"))

    with open(osp.join(base_dir, "configs.json")) as jsonfile:
        configs = json.load(jsonfile)

    class2label_path = osp.join(base_dir, "class2label.json")
    class2label_mapping = {}
    if osp.exists(class2label_path):
        try:
            with open(class2label_path) as jsonfile:
                class2label_mapping = json.load(jsonfile)
                print("Class to label file loaded!")
        except Exception as e:
            print("Class to label file invalid!")
            class2label_mapping = {}
    else:
        print("Class to label file not found!")

    # TODO: Remove this in the future
    network_type = "resnet-18-32x32"
    expected_input_shape = MODEL_INPUT_SHAPE.get(network_type)
    image_size = (
        configs["image_size"] if expected_input_shape is None else expected_input_shape
    )

    print("Server initializing...")

    """ CREATE SERVER """
    server = RServer.create_server(
        configs=configs,
        base_dir=base_dir,
        dataset_dir=dataset_dir,
        ckpt_dir=ckpt_dir,
        app=app,
        socket=socket,
    )

    """ SETUP DATA MANAGER """
    # Setup database
    from database.db_init import db, init_db

    init_db(app, db_path)

    # Setup data manager
    data_manager = RDataManager(
        base_dir,
        dataset_dir,
        db,
        app,
        image_size=image_size,
        image_padding=configs["image_padding"],
        class2label_mapping=class2label_mapping,
    )
    RServer.set_data_manager(data_manager)

    """ SETUP MODEL """
    # TODO：Remove this in the future
    configs["weight_to_load"] = "dummy_weight.pth"
    configs["pre_trained"] = False
    model = RModelWrapper(
        db_conn=db,
        network_type=network_type,
        net_path=to_unix(os.path.join(ckpt_dir, configs["weight_to_load"])),
        device=configs["device"],
        pretrained=configs["pre_trained"],
        num_classes=configs["num_classes"],
        app=app,
    )
    RServer.set_model(model)

    """ SETUP AUTO ANNOTATOR """
    checkpoint_name = "u2net.pth"
    annotator = RAutoAnnotator(
        configs["device"],
        checkpoint=osp.join(base_dir, checkpoint_name),
        model_name="u2net",
    )
    RServer.set_auto_annotator(annotator)

    print("Performing server consistency checks...")

    # Check file state consistency
    precheck()


def get_args():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--basedir",
        default="/Robustar2",
        help="path to base directory for data folder (default: /Robustar2)",
    )

    args = parser.parse_known_args()[0]
    return args


def create_app():
    args = get_args()

    # Get basedir
    basedir = to_absolute(os.getcwd(), to_unix(args.basedir))
    print("Current working directory is {}".format(os.getcwd()))
    print("Absolute basedir is {}".format(basedir))
    new_server_object(basedir, app, socket)

    print("Server started")
    return RServer.get_server().get_flask_app()


if __name__ == "__main__":
    # Start server
    create_app().run(port="8000", host="0.0.0.0", debug=False)
